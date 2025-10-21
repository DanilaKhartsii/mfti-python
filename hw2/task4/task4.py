try:
    with open("input.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    unique_lines = set(line.strip() for line in lines)

    with open("unique_output.txt", "w", encoding="utf-8") as file:
        for line in unique_lines:
            file.write(line + "\n")

    print("Уникальные строки успешно записаны в unique_output.txt.")
except FileNotFoundError:
    print("Ошибка: файл input.txt не найден.")
