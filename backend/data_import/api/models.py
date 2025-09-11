from typing import cast

from pydantic import ConfigDict, model_validator
from sqlmodel import SQLModel

from app.models.schools import (
    EtapEdukacjiBase,
    KategoriaUczniowBase,
    StatusPublicznoprawnyBase,
    SzkolaExtendedData,
    TypSzkolyBase,
)
from data_import.api.types import SchoolDict
from data_import.utils.convert_to_camel import custom_camel


class GeolocationAPIResponse(SQLModel):
    latitude: float
    longitude: float


class SzkolaAPIResponse(SzkolaExtendedData):
    model_config: ConfigDict = ConfigDict(alias_generator=custom_camel)  # pyright: ignore[reportIncompatibleVariableOverride]
    geolokalizacja: GeolocationAPIResponse
    typ: TypSzkolyBase
    status_publiczno_prawny: StatusPublicznoprawnyBase
    etapy_edukacji: list[EtapEdukacjiBase] | None
    wojewodztwo: str
    wojewodztwo_kod_TERYT: str  # noqa: N815
    powiat: str
    powiat_kod_TERYT: str  # noqa: N815
    gmina: str
    gmina_kod_TERYT: str  # noqa: N815
    miejscowosc: str
    miejscowosc_kod_TERYT: str  # noqa: N815
    ulica: str | None
    ulica_kod_TERYT: str | None  # noqa: N815
    ksztalcenie_zawodowe: dict[str, str] | None
    kategoria_uczniow: KategoriaUczniowBase

    @model_validator(mode="before")
    @classmethod
    def empty_str_list_to_none[T](cls, data: T) -> T:
        """Convert empty strings and empty lists to None for all fields."""
        if not isinstance(data, dict):
            raise ValueError(f"Expected data to be a dictionary, but got {data}")

        # Convert empty strings to None for all fields
        for field_name, field_value in list(cast(SchoolDict, data).items()):
            if (
                field_value == "" or field_value == []
            ):  # "" or [] are considered empty, 0 is a normal value
                data[field_name] = None

        return cast(T, data)
