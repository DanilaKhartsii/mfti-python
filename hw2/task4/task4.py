try:
    with open("input.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    lines = [line.strip() for line in lines]

    unique_once = [line for line in lines if lines.count(line) == 1]

    with open("unique_output.txt", "w", encoding="utf-8") as file:
        for line in unique_once:
            file.write(line + "\n")

    print("Строки, встречающиеся один раз, записаны в unique_output.txt.")
except FileNotFoundError:
    print("Ошибка: файл input.txt не найден.")
