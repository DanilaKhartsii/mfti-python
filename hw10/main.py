from fastapi import FastAPI, HTTPException
from .database import Database
from .schemas import StudentCreate, StudentUpdate, StudentResponse

app = FastAPI()
db = Database()


@app.post("/students/", response_model=StudentResponse)
def create_student(data: StudentCreate):
    student_id = db.create_student(data.name, data.faculty)
    student = db.get_student(student_id)
    return StudentResponse(
        id=student.id,
        name=student.name,
        faculty=student.faculty.name
    )


@app.get("/students/{student_id}", response_model=StudentResponse)
def read_student(student_id: int):
    student = db.get_student(student_id)
    if not student:
        raise HTTPException(404, "Студент не найден")
    return StudentResponse(
        id=student.id,
        name=student.name,
        faculty=student.faculty.name
    )


@app.get("/students/")
def list_students():
    return [
        {
            "id": s.id,
            "name": s.name,
            "faculty": s.faculty.name
        }
        for s in db.get_all_students()
    ]


@app.put("/students/{student_id}", response_model=StudentResponse)
def update_student(student_id: int, data: StudentUpdate):
    student = db.update_student(
        student_id, data.name, data.faculty
    )

    if not student:
        raise HTTPException(404, "Студент не найден")

    return StudentResponse(
        id=student.id,
        name=student.name,
        faculty=student.faculty.name
    )


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    ok = db.delete_student(student_id)
    if not ok:
        raise HTTPException(404, "Студент не найден")
    return {"status": "deleted"}
