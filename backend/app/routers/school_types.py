from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.core.database import get_session
from app.models.schools import TypSzkoly, TypSzkolyPublic

SessionDep = Annotated[Session, Depends(get_session)]

router = APIRouter(
    prefix="/school_types",
    tags=["school_types"],
)


@router.get("/", response_model=list[TypSzkolyPublic])
async def read_school_types(session: SessionDep, name: str | None = None):
    """
    Fetch all available school types or just one type if type name is provided.
    """
    statement = select(TypSzkoly)
    if name:
        statement = statement.where(TypSzkoly.nazwa == name)
    school_types = session.exec(statement).all()
    if name and not school_types:
        raise HTTPException(status_code=404, detail="School type not found")
    return school_types


@router.get("/{school_type_id}", response_model=TypSzkolyPublic)
async def read_school_type_by_id(school_type_id: int, session: SessionDep):
    school_type = session.get(TypSzkoly, school_type_id)
    if not school_type:
        raise HTTPException(status_code=404, detail="School type not found")
    return school_type
