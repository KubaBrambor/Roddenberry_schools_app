from enum import Enum
from typing import ClassVar, final

from app.models.exam_results import WynikE8, WynikEM


class APISettings:
    API_SCHOOLS_URL: str = "https://api-rspo.men.gov.pl/api/placowki/"
    HEADERS: ClassVar[dict[str, str]] = {"accept": "application/ld+json"}
    START_PAGE: int = 1
    PAGE_LIMIT: int | None = None  # the last page to fetch, if None there is no limit
    MAX_SCHOOLS_SEGMENT: int = 1000


class RetrySettings:
    INITIAL_DELAY: int = 1
    MAX_DELAY: int = 30
    MAX_RETRIES: int = 20


class TIMEOUT:
    CONNECT: int = 30
    READ: int = 60


@final
class ExamType(Enum):
    "Directories for E8 and EM data and their headers"

    E8 = ("E8_data", [0, 1], None)
    EM = ("EM_data", [1, 2], 0)

    def __init__(self, directory_name: str, header: list[int], skip_rows: int | None):
        self.directory_name = directory_name
        self.header = header
        self.skiprows = skip_rows


@final
class ExcelFile:
    SHEET_NAME = "SAS"
    SPECIAL_COLUMN_START = ("Unnamed", "dla")


@final
class ScoreType(Enum):
    E8 = (
        {
            "jezyk_polski": 0.3,
            "matematyka": 0.4,
            "jezyk_angielski": 0.3,
        },
        WynikE8,
    )
    EM = (
        {
            "jezyk_polski_poziom_podstawowy": 0.25,
            "matematyka_poziom_podstawowy": 0.3,
            "jezyk_angielski_poziom_podstawowy": 0.25,
            "jezyk_angielski_poziom_rozszerzony": 0.1,
            "matematyka_poziom_rozszerzony": 0.1,
        },
        WynikEM,
    )

    def __init__(
        self, subject_weights_map: dict[str, float], table_type: type[WynikE8 | WynikEM]
    ):
        self.subject_weights_map = subject_weights_map
        self.table_type = table_type
