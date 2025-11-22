from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel, UniqueConstraint

if TYPE_CHECKING:
    from app.models.schools import Szkola


class PrzedmiotBase(SQLModel):
    nazwa: str = Field(index=True, unique=True)


class Przedmiot(PrzedmiotBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    wyniki_e8: list["WynikE8"] = Relationship(back_populates="przedmiot")  # pyright: ignore[reportAny]
    wyniki_em: list["WynikEM"] = Relationship(back_populates="przedmiot")  # pyright: ignore[reportAny]


class PrzedmiotPublic(PrzedmiotBase):
    id: int


# Columns that default to None don't always exist in excel files
class WynikBase(SQLModel):
    liczba_zdajacych: int | None
    mediana: float | None = None


class WynikE8Extra(WynikBase):
    wynik_sredni: float | None


class WynikEMExtra(WynikBase):
    sredni_wynik: float | None
    zdawalnosc: float | None = None
    liczba_laureatow_finalistow: int | None = None


class WynikCommon(WynikBase):
    szkola_id: int = Field(index=True, foreign_key="szkola.id")
    przedmiot_id: int = Field(index=True, foreign_key="przedmiot.id")
    rok: int = Field(index=True)


class WynikE8(WynikE8Extra, WynikCommon, table=True):
    __tablename__: str = "wynik_e8"  # pyright: ignore[reportIncompatibleVariableOverride]
    __table_args__: tuple[UniqueConstraint] = (
        UniqueConstraint(
            "szkola_id",
            "przedmiot_id",
            "rok",
            name="uq_wynik_e8_szkola_przedmiot_rok",
        ),
    )
    id: int | None = Field(default=None, primary_key=True)
    liczba_zdajacych: int  # pyright: ignore[reportIncompatibleVariableOverride]
    przedmiot: Przedmiot = Relationship(back_populates="wyniki_e8")  # pyright: ignore[reportAny]
    szkola: "Szkola" = Relationship(back_populates="wyniki_e8")  # pyright: ignore[reportAny]


class WynikE8Public(WynikCommon, WynikE8Extra):
    id: int


class WynikE8PublicWithPrzedmiot(WynikE8Public):
    przedmiot: PrzedmiotPublic


class WynikEM(WynikEMExtra, WynikCommon, table=True):
    __tablename__: str = "wynik_em"  # pyright: ignore[reportIncompatibleVariableOverride]
    __table_args__: tuple[UniqueConstraint] = (
        UniqueConstraint(
            "szkola_id",
            "przedmiot_id",
            "rok",
            name="uq_wynik_em_szkola_przedmiot_rok",
        ),
    )
    id: int | None = Field(default=None, primary_key=True)
    liczba_zdajacych: int  # pyright: ignore[reportIncompatibleVariableOverride]
    przedmiot: Przedmiot = Relationship(back_populates="wyniki_em")  # pyright: ignore[reportAny]
    szkola: "Szkola" = Relationship(back_populates="wyniki_em")  # pyright: ignore[reportAny]


class WynikEMPublic(WynikCommon, WynikEMExtra):
    id: int


class WynikEMPublicWithPrzedmiot(WynikEMPublic):
    przedmiot: PrzedmiotPublic
