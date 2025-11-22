from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.bounding_box import BoundingBox
from app.models.exam_results import (
    WynikE8PublicWithPrzedmiot,  # noqa: F401
    WynikEMPublicWithPrzedmiot,  # noqa: F401
)
from app.models.schools import (
    Szkola,
    SzkolaPublicShort,
    SzkolaPublicWithRelations,
)
from dependencies import parse_bbox

_ = SzkolaPublicWithRelations.model_rebuild()

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/schools",
    tags=["schools"],
)


@router.get("/{school_id}", response_model=SzkolaPublicWithRelations)
async def read_school(school_id: int, session: SessionDep) -> Szkola:
    school = session.get(Szkola, school_id)
    if not school:
        raise HTTPException(status_code=404, detail="School not found")
    return school


class FilterParams(BoundingBox):
    type: int | None = None


@router.get("/", response_model=list[SzkolaPublicShort])
async def read_schools(
    session: SessionDep,
    bbox: Annotated[BoundingBox, Depends(parse_bbox)],
    school_type: Annotated[int | None, Query(alias="type")] = None,
):
    # SQL query to filter schools within bounding box boundaries
    statement = select(Szkola).where(
        (Szkola.geolokalizacja_latitude >= bbox.min_lat)
        & (Szkola.geolokalizacja_latitude <= bbox.max_lat)
        & (Szkola.geolokalizacja_longitude >= bbox.min_lng)
        & (Szkola.geolokalizacja_longitude <= bbox.max_lng)
    )

    # Add type filter if type parameter is provided
    if school_type is not None:
        statement = statement.where(Szkola.typ_id == school_type)

    schools = session.exec(statement).all()
    return schools
