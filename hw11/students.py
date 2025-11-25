from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import get_db
from .auth import get_current_user, require_write_access

router = APIRouter(
    prefix="/students",
    tags=["students"],
    dependencies=[Depends(get_current_user)],
)


@router.post(
    "/", response_model=schemas.StudentResponse, dependencies=[Depends(require_write_access)]
)
def create_student(
    student_in: schemas.StudentCreate,
    db: Session = Depends(get_db),
):
    student = models.Student(
        name=student_in.name,
        faculty=student_in.faculty,
        course=student_in.course,
    )
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.get("/", response_model=List[schemas.StudentResponse])
def list_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()
    return students


@router.get("/{student_id}", response_model=schemas.StudentResponse)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).get(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return student


@router.put(
    "/{student_id}",
    response_model=schemas.StudentResponse,
    dependencies=[Depends(require_write_access)],
)
def update_student(
    student_id: int,
    student_in: schemas.StudentUpdate,
    db: Session = Depends(get_db),
):
    student = db.query(models.Student).get(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )

    if student_in.name is not None:
        student.name = student_in.name
    if student_in.faculty is not None:
        student.faculty = student_in.faculty
    if student_in.course is not None:
        student.course = student_in.course

    db.add(student)
    db.commit()
    db.refresh(student)
    return student


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_write_access)],
)
def delete_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(models.Student).get(student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    db.delete(student)
    db.commit()
