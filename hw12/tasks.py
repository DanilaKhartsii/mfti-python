import csv
from typing import List
from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from .database import get_db
from .models import Student
from .auth import get_current_user, require_write_access
from .cache import cache_delete_pattern

router = APIRouter(prefix="/tasks", tags=["tasks"])


def load_csv_background(file_path: str, db: Session):
    with open(file_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            student = Student(
                name=row["name"],
                faculty=row["faculty"],
                course=int(row["course"])
            )
            db.add(student)
        db.commit()

    cache_delete_pattern("students*")


def delete_students_background(ids: List[int], db: Session):
    for student_id in ids:
        obj = db.query(Student).filter(Student.id == student_id).first()
        if obj:
            db.delete(obj)
    db.commit()

    cache_delete_pattern("students*")


@router.post("/load_csv")
def load_csv(
    file_path: str,
    background: BackgroundTasks,
    db: Session = Depends(get_db),
    user=Depends(require_write_access),
):
    background.add_task(load_csv_background, file_path, db)
    return {"status": "started", "task": "load_csv"}


@router.post("/delete_students")
def delete_students(
    ids: List[int],
    background: BackgroundTasks,
    db: Session = Depends(get_db),
    user=Depends(require_write_access),
):
    background.add_task(delete_students_background, ids, db)
    return {"status": "started", "task": "delete_students"}
