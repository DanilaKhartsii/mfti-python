from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import schemas, models
from .database import get_db
from .auth import get_current_user, require_write_access
from .cache import cache_get, cache_set, cache_delete_pattern

router = APIRouter(
    prefix="/students",
    tags=["students"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=List[schemas.StudentResponse])
def list_students(db: Session = Depends(get_db)):
    key = "students_all"

    cached = cache_get(key)
    if cached:
        return cached

    qs = db.query(models.Student).all()
    result = [schemas.StudentResponse.from_orm(s) for s in qs]
    cache_set(key, [r.dict() for r in result])
    return result


@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    key = f"students_{student_id}"

    cached = cache_get(key)
    if cached:
        return cached

    student = db.query(models.Student).get(student_id)
    if not student:
        raise HTTPException(404, "Student not found")

    result = schemas.StudentResponse.from_orm(student)
    cache_set(key, result.dict())
    return result


@router.post("/", response_model=schemas.StudentResponse, dependencies=[Depends(require_write_access)])
def create_student(student_in: schemas.StudentCreate, db: Session = Depends(get_db)):
    student = models.Student(
        name=student_in.name,
        faculty=student_in.faculty,
        course=student_in.course,
    )
    db.add(student)
    db.commit()
    db.refresh(student)

    cache_delete_pattern("students*")

    return student
