from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.locations import Gmina, Miejscowosc, Powiat
from app.models.schools import Szkola, SzkolaPublic, SzkolaPublicShort

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/schools",
    tags=["schools"],
)


@router.get("/{school_id}", response_model=SzkolaPublic)
async def read_school(school_id: int, session: SessionDep) -> Szkola:
    school = session.get(Szkola, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school


@router.get("/", response_model=list[SzkolaPublicShort])
async def read_schools(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
    voivodeship_id: Annotated[int | None, Query(gt=0, le=16)] = None,
):
    if voivodeship_id:  # retrieve all schools from a single voivodeship
        statement = (
            select(Szkola)
            .join(Miejscowosc)
            .join(Gmina)
            .join(Powiat)
            .where(Powiat.wojewodztwo_id == voivodeship_id)
        )
        schools = session.exec(statement).all()
        return schools
    # if voivodship_id is not provided, return a page of schools
    schools = session.exec(select(Szkola).offset(skip).limit(limit)).all()
    return schools
