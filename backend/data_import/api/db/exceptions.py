from pydantic import ValidationError

from data_import.api.types import SchoolDict


class DataValidationError(Exception):
    """Raised when incoming school_data fails Pydantic validation."""

    raw_data: SchoolDict
    original_exc: ValidationError

    def __init__(self, raw_data: SchoolDict, original_exc: ValidationError):
        super().__init__(f"Validation failed for {raw_data}: {original_exc}")
        self.raw_data = raw_data
        self.original_exc = original_exc


class SchoolProcessingError(Exception):
    """Raised when something goes wrong during DB/session processing."""

    rspo: int
    original_exc: Exception

    def __init__(self, rspo: int, original_exc: Exception):
        super().__init__(f"Error processing school RSPO={rspo}: {original_exc}")
        self.rspo = rspo
        self.original_exc = original_exc
