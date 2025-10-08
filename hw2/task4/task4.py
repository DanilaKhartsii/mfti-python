try:
    with open("input.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    unique_lines = []
    for line in lines:
        if line not in unique_lines:
            unique_lines.append(line)

    with open("unique_output.txt", "w", encoding="utf-8") as file:
        file.writelines(unique_lines)

    print("Уникальные строки записаны в unique_output.txt.")
except FileNotFoundError:
    print("Ошибка: файл input.txt не найден.")
