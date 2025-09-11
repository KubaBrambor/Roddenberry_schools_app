from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.schools import Szkola


class WojewodztwoBase(SQLModel):
    nazwa: str = Field(index=True)
    teryt: str = Field(index=True, unique=True)


class Wojewodztwo(WojewodztwoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    powiaty: list["Powiat"] = Relationship(back_populates="wojewodztwo")  # pyright: ignore [reportAny]


class WojewodztwoPublic(WojewodztwoBase):
    id: int


class PowiatBase(SQLModel):
    nazwa: str = Field(index=True)
    teryt: str = Field(index=True, unique=True)
    wojewodztwo_id: int | None = Field(
        index=True, default=None, foreign_key="wojewodztwo.id"
    )


class Powiat(PowiatBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    wojewodztwo: Wojewodztwo = Relationship(back_populates="powiaty")  # pyright: ignore [reportAny]
    gminy: list["Gmina"] = Relationship(back_populates="powiat")  # pyright: ignore [reportAny]


class PowiatPublic(PowiatBase):
    id: int


class GminaBase(SQLModel):
    nazwa: str = Field(index=True)
    teryt: str = Field(index=True, unique=True)
    powiat_id: int | None = Field(index=True, default=None, foreign_key="powiat.id")


class Gmina(GminaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    powiat: Powiat = Relationship(back_populates="gminy")  # pyright: ignore [reportAny]
    miejscowosci: list["Miejscowosc"] = Relationship(back_populates="gmina")  # pyright: ignore [reportAny]


class GminaPublic(GminaBase):
    id: int


class MiejscowoscBase(SQLModel):
    nazwa: str = Field(index=True)
    teryt: str = Field(index=True, unique=True)
    gmina_id: int | None = Field(index=True, default=None, foreign_key="gmina.id")


class Miejscowosc(MiejscowoscBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    gmina: Gmina = Relationship(back_populates="miejscowosci")  # pyright: ignore [reportAny]
    szkoly: list["Szkola"] = Relationship(back_populates="miejscowosc")  # pyright: ignore [reportAny]


class MiejscowoscPublic(MiejscowoscBase):
    id: int


class UlicaBase(SQLModel):
    nazwa: str = Field(index=True)
    teryt: str = Field(index=True, unique=True)


class Ulica(UlicaBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    szkoly: list["Szkola"] = Relationship(back_populates="ulica")  # pyright: ignore [reportAny]


class UlicaPublic(UlicaBase):
    id: int
