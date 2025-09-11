import logging
from typing import cast

from sqlmodel import select

from app.models.exam_results import Przedmiot, WynikE8
from app.models.schools import Szkola
from data_import.core.config import ScoreType
from data_import.score.types import WynikTable
from data_import.utils.db.session import DatabaseManagerBase

logger = logging.getLogger(__name__)


class Scorer(DatabaseManagerBase):
    _subject_weights_map: dict[str, float]
    _schools_ids: list[int]
    _subjects: list[Przedmiot]
    _years_num: int = 0
    _table_type: type[WynikTable]

    def __init__(self, score_type: ScoreType):
        super().__init__()
        self._subject_weights_map = score_type.subject_weights_map
        self._table_type = score_type.table_type
        self._schools_ids = []
        self._subjects = []

    def _load_school_ids(self):
        session = self._ensure_session()
        ids = cast(
            list[int], session.exec(select(self._table_type.szkola_id)).unique().all()
        )
        if not ids:
            raise ValueError("No school IDs found in the database.")
        self._schools_ids = ids

    def _load_subjects(self):
        session = self._ensure_session()
        subject_names = list(self._subject_weights_map.keys())
        statement = select(Przedmiot).where(Przedmiot.nazwa.in_(subject_names))  # pyright: ignore[reportAttributeAccessIssue, reportUnknownMemberType, reportUnknownArgumentType]
        self._subjects = list(session.exec(statement).all())
        if not self._subjects:
            raise ValueError("No subjects found in the database.")
        elif len(self._subjects) != len(subject_names):
            raise ValueError(
                f"Not all subjects found in the database. Found: {self._subjects}. Expected: {subject_names}"
            )

    def _get_number_of_years(self):
        session = self._ensure_session()
        years = session.exec(select(self._table_type.rok)).unique().all()
        if not years:
            raise ValueError("No years found in the database.")
        self._years_num = len(years)

    def _initialize_required_data(self):
        self._load_school_ids()
        self._load_subjects()
        self._get_number_of_years()  # count all distinct years from the table with scores

    def _calculate_subject_score(self, subject: Przedmiot, school_id: int) -> float:
        session = self._ensure_session()
        statement = select(self._table_type).where(
            self._table_type.szkola_id == school_id,
            self._table_type.przedmiot_id == subject.id,
        )
        subject_results = session.exec(statement).all()
        if not subject_results:
            logger.warning(
                f"🤔 No results found for school ID {school_id}, subject '{subject.nazwa}'. Assigning score 0 for this subject's contribution."
            )
            return 0

        # there should be the same amount of records as years
        if len(subject_results) != self._years_num:
            logger.info(
                f"🗓️ Data mismatch for school ID {school_id}, subject '{subject.nazwa}': Found {len(subject_results)} results, expected for {self._years_num} years. Proceeding with available data."
            )
        # calculate weighted median
        numerator = 0.0
        denominator = 0.0
        for result in subject_results:
            value = result.mediana
            if (
                value is None
            ):  # if there is no median use sredni_wynik for WynikEM and wynik_sredni for WynikE8
                value = cast(
                    float,
                    result.wynik_sredni
                    if isinstance(result, WynikE8)
                    else result.sredni_wynik,
                )
            numerator += value * result.liczba_zdajacych
            denominator += result.liczba_zdajacych

        if denominator == 0:
            logger.warning(
                f"🔢 Denominator is zero for school ID {school_id}, subject '{subject.nazwa}' (total 'liczba_zdajacych' is 0). Assigning score 0 for this subject."
            )
            return 0.0

        return numerator / denominator

    def calculate_scores(self):
        session = self._ensure_session()
        try:
            self._initialize_required_data()
        except ValueError as e:
            logger.error(
                f"⚙️ Initialization error: {e}. Aborting school scoring process."
            )
            return
        # then get all records for specific school and specific subject -> calculate score for this subject
        for id in self._schools_ids:
            final_score = 0.0  # final score for every school after calculating results from all subjects
            for subject in self._subjects:
                subject_score = self._calculate_subject_score(subject, id)
                weight = self._subject_weights_map[subject.nazwa]
                final_score += subject_score * weight
            school = self._select_where(Szkola, Szkola.id == id)
            if not school:
                logger.error(
                    f"🔍 School with ID {id} not found in database. Cannot update score."
                )
                continue
            school.score = final_score
            session.add(school)
            session.commit()
            logger.info(
                f"🎯 Score updated for school (RSPO: {school.numer_rspo}): {final_score:.2f}"
            )
