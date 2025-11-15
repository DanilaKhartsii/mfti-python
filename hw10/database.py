import csv
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from .models import Base, Faculty, Student, Course, Grade


class Database:
    def __init__(self, url="sqlite:///students.db"):
        self.engine = create_engine(url, echo=False)
        Base.metadata.create_all(self.engine)

    def insert_from_csv(self, filename):
        with Session(self.engine) as session, open(filename, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                full_name = f"{row['Фамилия']} {row['Имя']}"
                faculty_name = row["Факультет"]
                course_name = row["Курс"]
                grade_value = float(row["Оценка"])

                faculty = session.query(Faculty).filter_by(name=faculty_name).first()
                if not faculty:
                    faculty = Faculty(name=faculty_name)
                    session.add(faculty)

                student = (
                    session.query(Student)
                    .filter_by(name=full_name, faculty=faculty)
                    .first()
                )
                if not student:
                    student = Student(name=full_name, faculty=faculty)
                    session.add(student)

                course = session.query(Course).filter_by(name=course_name).first()
                if not course:
                    course = Course(name=course_name)
                    session.add(course)

                session.flush()

                grade = Grade(student=student, course=course, value=grade_value)
                session.add(grade)

            session.commit()

    # -------------------------------
    # CREATE
    # -------------------------------
    def create_student(self, name, faculty_name):
        with Session(self.engine) as session:
            faculty = session.query(Faculty).filter_by(name=faculty_name).first()
            if not faculty:
                faculty = Faculty(name=faculty_name)
                session.add(faculty)
                session.flush()

            student = Student(name=name, faculty=faculty)
            session.add(student)
            session.commit()
            return student.id

    def get_student(self, student_id):
        with Session(self.engine) as session:
            return session.get(Student, student_id)

    def get_all_students(self):
        with Session(self.engine) as session:
            stmt = select(Student)
            return [s for s in session.execute(stmt).scalars()]

    def update_student(self, student_id, new_name=None, new_faculty=None):
        with Session(self.engine) as session:
            student = session.get(Student, student_id)
            if not student:
                return None

            if new_name:
                student.name = new_name

            if new_faculty:
                faculty = session.query(Faculty).filter_by(name=new_faculty).first()
                if not faculty:
                    faculty = Faculty(name=new_faculty)
                    session.add(faculty)
                student.faculty = faculty

            session.commit()
            return student

    def delete_student(self, student_id):
        with Session(self.engine) as session:
            student = session.get(Student, student_id)
            if not student:
                return False
            session.delete(student)
            session.commit()
            return True
