from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey

Base = declarative_base()


class Faculty(Base):
    __tablename__ = "faculties"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    students = relationship("Student", back_populates="faculty")


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    faculty_id = Column(Integer, ForeignKey("faculties.id"))

    faculty = relationship("Faculty", back_populates="students")
    grades = relationship("Grade", back_populates="student")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    grades = relationship("Grade", back_populates="course")


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    course_id = Column(Integer, ForeignKey("courses.id"))
    value = Column(Float, nullable=False)

    student = relationship("Student", back_populates="grades")
    course = relationship("Course", back_populates="grades")
