# pyright: reportUnknownParameterType = false
# pyright: reportUnknownMemberType = false
# pyright: reportUnknownVariableType = false
# pyright: reportMissingTypeArgument = false
# pyright: reportUnknownArgumentType = false
import logging
from collections.abc import Hashable

import pandas as pd
from pydantic import ValidationError

from app.models.exam_results import (
    Przedmiot,
    WynikE8,
    WynikE8Extra,
    WynikEM,
    WynikEMExtra,
)
from app.models.schools import Szkola
from data_import.core.config import ExamType, ExcelFile
from data_import.utils.clean_column_names import clean_column_name
from data_import.utils.db.session import DatabaseManagerBase

logger = logging.getLogger(__name__)


class TableSplitter(DatabaseManagerBase):
    exam_data: pd.DataFrame
    rspo_col_name: tuple[str, str] = ("", "")
    unique_subjects: set[str]
    exam_type: ExamType
    year: int
    subjects_cache: dict[str, Przedmiot]
    processed_count: int = 0
    skipped_schools: int = 0
    added_results: int = 0

    def __init__(self, exam_data: pd.DataFrame, exam_type: ExamType, year: int):
        super().__init__()
        self.exam_data = exam_data
        self.exam_type = exam_type
        self.year = year
        self.unique_subjects = set()
        self.subjects_cache = {}

    def initialize(self) -> bool:
        """Perform initialization and validation steps.
        Returns True if successful, False otherwise."""
        try:
            self._get_rspo_col_name()
            self._get_subjects_names()
            return True
        except ValueError as e:
            logger.error(
                f"❌ Initialization failed: {e}. Skipping processing for this file."
            )
            return False

    def _get_rspo_col_name(self):
        rspo_cols = [
            col
            for col in self.exam_data.columns
            if isinstance(col, tuple)
            and "RSPO" in col[1]  # RSPO is in the second part of the tuple
        ]
        if len(rspo_cols) != 1:
            raise ValueError("Exactly one column with 'RSPO' in its name is expected.")
        self.rspo_col_name = rspo_cols[0]

    def _get_subjects_names(self):
        """
        Extracts unique subject names from the multi-level column index,
        prunes exam data to include only subjects of interest.
        Assumes subject names are in the first level.
        """

        # Iterate through columns to find subjects (assuming they are level 0 of multi-index)
        for col in self.exam_data.columns:
            # Check if it's a tuple (multi-index) and not unnamed/metadata column which can be skipped
            if isinstance(col, tuple) and len(col) > 1:
                valid_col = True
                for col_prefix in ExcelFile.SPECIAL_COLUMN_START:
                    if col_prefix in col[0]:
                        valid_col = False
                        break
                if not valid_col:
                    continue
                self.unique_subjects.add(str(col[0]))

        logger.info(f"📚 Identified subjects for processing: {self.unique_subjects}")
        cols_to_keep = [*self.unique_subjects, self.rspo_col_name[0]]

        # slicing of self.exam_data to get only exam results + rspo column
        self.exam_data = self.exam_data.loc[:, cols_to_keep]

    def get_subject(self, subject_name: str) -> Przedmiot:
        """Gets a Przedmiot record in the database. If it does not exist, creates it."""
        if subject_name in self.subjects_cache:
            return self.subjects_cache[subject_name]

        subject = self._select_where(Przedmiot, Przedmiot.nazwa == subject_name)
        if subject:
            self.subjects_cache[subject_name] = subject
            return subject

        # no record found
        self.create_subject(subject_name)
        return self.subjects_cache[subject_name]

    def create_subject(self, subject_name: str):
        """Creates a Przedmiot record in the database."""
        logger.info(f"✨ Creating new subject (Przedmiot): {subject_name}")
        subject = Przedmiot(nazwa=subject_name)
        self.subjects_cache[subject_name] = subject

    def get_school_rspo_number(
        self, school_exam_data: pd.Series, index: Hashable
    ) -> int | None:
        # Extract RSPO number from the current row
        rspo = school_exam_data.at[self.rspo_col_name]

        if pd.isna(rspo):
            self.skip_school(f"❓ RSPO number not found in row {index}")
            return None
        return int(rspo)

    def get_school(self, rspo: int) -> Szkola | None:
        school = self._select_where(Szkola, Szkola.numer_rspo == rspo)
        if not school:
            self.skip_school(f"❓ School with RSPO {rspo} not found in the database")
        return school

    def skip_school(self, reason: str):
        logger.warning(
            f"{reason}. Therefore, skipping associated results for this school."
        )
        self.skipped_schools += 1

    def _validate_enough_data(self, result: WynikE8Extra | WynikEMExtra) -> bool:
        # the columns differ in different exam types
        average_score: float | None = (
            result.sredni_wynik
            if isinstance(result, WynikEMExtra)
            else result.wynik_sredni
        )
        if (
            not result.liczba_zdajacych
        ):  # even if liczba_zdajacych is 0 we are dismissing the result
            return False
        if average_score is None and result.mediana is None:  # score can equal to 0
            return False
        return True

    def create_result_record(
        self,
        subject_exam_result: dict[str, int | float | None],
        school: Szkola,
        subject: Przedmiot,
        base: type[WynikE8Extra | WynikEMExtra],
        table: type[WynikE8 | WynikEM],
    ) -> WynikE8 | WynikEM | None:
        session = self._ensure_session()
        try:
            result_base = base.model_validate(subject_exam_result)
        except ValidationError as e:
            logger.error(
                f"🚫 Invalid data for subject '{subject.nazwa}' (School RSPO: {school.numer_rspo}). Details: {subject_exam_result}. Error: {e}"
            )
            return None
        if not self._validate_enough_data(result_base):
            logger.warning(
                f"📊 Insufficient data for '{subject.nazwa}' (Details: {subject_exam_result}). Skipping result record creation."
            )
            return None
        result = table(
            szkola=school,
            przedmiot=subject,
            rok=self.year,
            **result_base.model_dump(),  # pyright: ignore[reportAny]
        )
        session.add(result)
        self.added_results += 1
        return result

    def create_results(self, school_exam_data: pd.Series, szkola: Szkola, rspo: int):
        session = self._ensure_session()
        results_to_commit = 0
        for subject_name in self.unique_subjects:
            subject = self.get_subject(clean_column_name(subject_name))

            subject_exam_result: dict[str, int | float | None] = (
                school_exam_data.loc[subject_name]
            ).to_dict()
            # change numpy NaN values to None and clean column names
            subject_exam_result = {
                clean_column_name(k): (v if pd.notna(v) else None)
                for k, v in subject_exam_result.items()
            }

            match self.exam_type:
                case ExamType.E8:
                    result = self.create_result_record(
                        subject_exam_result, szkola, subject, WynikE8Extra, WynikE8
                    )
                case ExamType.EM:
                    result = self.create_result_record(
                        subject_exam_result, szkola, subject, WynikEMExtra, WynikEM
                    )
            if not result:
                continue  # there was a ValidationError, move on
            results_to_commit += 1
            logger.info(f"💾 Added new exam result: {result.przedmiot} (RSPO: {rspo})")

        if results_to_commit > 0:
            session.commit()

    def split_exam_results(self):
        """
        Iterates through exam data, finds corresponding schools and subjects,
        creates WynikE8/WynikEM records, and adds them to the DB session.
        """
        logger.info(
            f"📊 Starting processing of {self.exam_type} results for {len(self.exam_data)} schools..."
        )

        for index, school_exam_data in self.exam_data.iterrows():
            school_exam_data: pd.Series
            try:
                # Find School by RSPO
                rspo = self.get_school_rspo_number(school_exam_data, index)
                if not rspo:
                    continue

                school = self.get_school(rspo)
                if not school:
                    continue

                # Process results for each subject for this school
                self.create_results(school_exam_data, school, rspo)

                self.processed_count += 1
                if self.processed_count % 100 == 0:  # Log progress periodically
                    logger.info(
                        f"⏳ Processed {self.processed_count} schools... Added {self.added_results} results so far."
                    )

            except Exception as e:
                logger.exception(f"📛 Unexpected error processing row {index}: {e}")
                self.skipped_schools += (
                    1  # Count as skipped if major error occurs for the row
                )

        logger.info(f"✅ Successfully processed {self.processed_count} schools.")
        logger.info(f"ℹ️ Added {self.added_results} new exam results to the session.")  # noqa: RUF001
        logger.info(
            f"ℹ️ Skipped {self.skipped_schools} schools due to missing/invalid RSPO, school not found in DB, or row processing error."  # noqa: RUF001
        )
