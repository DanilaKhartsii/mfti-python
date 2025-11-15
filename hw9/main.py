from database import Database

def main():
    db = Database()

    db.insert_from_csv("students.csv")

    print("\n--- Студенты по факультету ---")
    print(db.get_students_by_faculty("АВТФ"))

    print("\n--- Уникальные курсы ---")
    print(db.get_unique_courses())

    print("\n--- Средний балл по факультету ФПМИ ---")
    print(db.get_avg_grade_by_faculty("ФПМИ"))

    print("\n--- Студенты с оценкой < 30 по курсу 'Мат. Анализ' ---")
    print(db.get_students_below_30("Мат. Анализ"))


if __name__ == "__main__":
    main()
