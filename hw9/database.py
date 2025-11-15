import csv
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session

from models import Base, Faculty, Student, Course, Grade


class Database:
    def __init__(self, db_url="sqlite:///students.db"):
        self.engine = create_engine(db_url, echo=False)
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

    def get_students_by_faculty(self, faculty_name):
        with Session(self.engine) as session:
            stmt = (
                select(Student.name)
                .join(Faculty)
                .where(Faculty.name == faculty_name)
            )
            return [row[0] for row in session.execute(stmt)]

    def get_unique_courses(self):
        with Session(self.engine) as session:
            stmt = select(Course.name).distinct()
            return [row[0] for row in session.execute(stmt)]

    def get_avg_grade_by_faculty(self, faculty_name):
        with Session(self.engine) as session:
            stmt = (
                select(func.avg(Grade.value))
                .join(Student)
                .join(Faculty)
                .where(Faculty.name == faculty_name)
            )
            return session.scalar(stmt)

    def get_students_below_30(self, course_name):
        with Session(self.engine) as session:
            stmt = (
                select(Student.name, Grade.value)
                .join(Grade)
                .join(Course)
                .where(Course.name == course_name)
                .where(Grade.value < 30)
            )
            return session.execute(stmt).all()
