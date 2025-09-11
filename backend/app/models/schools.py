from typing import TYPE_CHECKING, Optional  # pyright: ignore[reportDeprecated]

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.exam_results import WynikE8, WynikEM
    from app.models.locations import Miejscowosc, Ulica


class TypSzkolyBase(SQLModel):
    nazwa: str = Field(index=True, unique=True)


class TypSzkoly(TypSzkolyBase, table=True):
    __tablename__: str = "typ_szkoly"  # pyright: ignore[reportIncompatibleVariableOverride]

    id: int | None = Field(default=None, primary_key=True)
    szkoly: list["Szkola"] = Relationship(back_populates="typ")  # pyright: ignore [reportAny]


class TypSzkolyPublic(TypSzkolyBase):
    id: int


class StatusPublicznoprawnyBase(SQLModel):
    nazwa: str = Field(index=True, unique=True)


class StatusPublicznoprawny(StatusPublicznoprawnyBase, table=True):
    __tablename__: str = "status_publicznoprawny"  # pyright: ignore[reportIncompatibleVariableOverride]

    id: int | None = Field(default=None, primary_key=True)
    szkoly: list["Szkola"] = Relationship(back_populates="status_publicznoprawny")  # pyright: ignore [reportAny]


class StatusPublicznoprawnyPublic(StatusPublicznoprawnyBase):
    id: int


class KategoriaUczniowBase(SQLModel):
    nazwa: str = Field(index=True, unique=True)


class KategoriaUczniow(KategoriaUczniowBase, table=True):
    __tablename__: str = "kategoria_uczniow"  # pyright: ignore[reportIncompatibleVariableOverride]

    id: int | None = Field(default=None, primary_key=True)
    szkoly: list["Szkola"] = Relationship(back_populates="kategoria_uczniow")  # pyright: ignore [reportAny]


# link table for connecting EtapyEdukacji and Szkoly
class SzkolaEtapLink(SQLModel, table=True):
    etap_id: int | None = Field(
        default=None, foreign_key="etap_edukacji.id", primary_key=True
    )
    szkola_id: int | None = Field(
        default=None, foreign_key="szkola.id", primary_key=True
    )


class EtapEdukacjiBase(SQLModel):
    nazwa: str = Field(index=True, unique=True)


class EtapEdukacji(EtapEdukacjiBase, table=True):
    __tablename__: str = "etap_edukacji"  # pyright: ignore[reportIncompatibleVariableOverride]

    id: int | None = Field(default=None, primary_key=True)
    szkoly: list["Szkola"] = Relationship(  # pyright: ignore [reportAny]
        back_populates="etapy_edukacji", link_model=SzkolaEtapLink
    )


class EtapEdukacjiPublic(EtapEdukacjiBase):
    id: int


class SzkolaKsztalcenieZawodoweLink(SQLModel, table=True):
    ksztalcenie_zawodowe_id: int | None = Field(
        default=None, foreign_key="ksztalcenie_zawodowe.id", primary_key=True
    )
    szkola_id: int | None = Field(
        default=None, foreign_key="szkola.id", primary_key=True
    )


class KsztalcenieZawodoweBase(SQLModel):
    nazwa: str = Field(index=True, unique=True)


class KsztalcenieZawodowe(KsztalcenieZawodoweBase, table=True):
    __tablename__: str = "ksztalcenie_zawodowe"  # pyright: ignore[reportIncompatibleVariableOverride]

    id: int | None = Field(default=None, primary_key=True)
    szkoly: list["Szkola"] = Relationship(  # pyright: ignore [reportAny]
        back_populates="ksztalcenie_zawodowe", link_model=SzkolaKsztalcenieZawodoweLink
    )


class SzkolaBase(SQLModel):
    numer_rspo: int = Field(unique=True, index=True)
    nazwa: str = Field(index=True)


class SzkolaExtendedData(SzkolaBase):  # used in SzkolaAPIResponse
    nip: str | None = Field(default=None)
    regon: str = Field(unique=True)
    liczba_uczniow: int | None = Field(default=None, ge=0)
    dyrektor_imie: str | None = Field(default=None)
    dyrektor_nazwisko: str | None = Field(default=None)
    kod_pocztowy: str
    numer_budynku: str | None = Field(default=None)
    numer_lokalu: str | None = Field(default=None)
    telefon: str | None = Field(
        default=None,
    )
    email: str | None = Field(
        default=None,
    )
    strona_internetowa: str | None = Field(default=None)


class SzkolaAllData(SzkolaExtendedData):
    geolokalizacja_latitude: float
    geolokalizacja_longitude: float
    score: float = Field(default=0.0)
    # Foreign keys
    typ_id: int | None = Field(index=True, default=None, foreign_key="typ_szkoly.id")
    status_publicznoprawny_id: int | None = Field(
        index=True, default=None, foreign_key="status_publicznoprawny.id"
    )
    kategoria_uczniow_id: int | None = Field(
        index=True, default=None, foreign_key="kategoria_uczniow.id"
    )
    miejscowosc_id: int | None = Field(
        index=True, default=None, foreign_key="miejscowosc.id"
    )
    ulica_id: int | None = Field(index=True, default=None, foreign_key="ulica.id")


class Szkola(SzkolaAllData, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # Relationships - many-to-one
    typ: TypSzkoly = Relationship(back_populates="szkoly")  # pyright: ignore [reportAny]
    status_publicznoprawny: StatusPublicznoprawny = Relationship(  # pyright: ignore [reportAny]
        back_populates="szkoly"
    )
    kategoria_uczniow: KategoriaUczniow = Relationship(back_populates="szkoly")  # pyright: ignore [reportAny]
    miejscowosc: "Miejscowosc" = Relationship(back_populates="szkoly")  # pyright: ignore [reportAny]
    ulica: Optional["Ulica"] = Relationship(back_populates="szkoly")  # pyright: ignore [reportAny, reportDeprecated]

    # Relationships - many-to-many
    etapy_edukacji: list[EtapEdukacji] = Relationship(  # pyright: ignore [reportAny]
        back_populates="szkoly", link_model=SzkolaEtapLink
    )
    ksztalcenie_zawodowe: list[KsztalcenieZawodowe] = Relationship(  # pyright: ignore [reportAny]
        back_populates="szkoly", link_model=SzkolaKsztalcenieZawodoweLink
    )
    wyniki_e8: list["WynikE8"] = Relationship(back_populates="szkola")  # pyright: ignore [reportAny]
    wyniki_em: list["WynikEM"] = Relationship(back_populates="szkola")  # pyright: ignore [reportAny]


class SzkolaPublic(SzkolaAllData):
    id: int


class SzkolaPublicShort(SzkolaBase):
    id: int
    geolokalizacja_latitude: float
    geolokalizacja_longitude: float
    score: float
    typ: TypSzkolyPublic
    status_publicznoprawny: StatusPublicznoprawnyPublic
