try:
    with open("text_file.txt", "r", encoding="utf-8") as file:
        text = file.read()
        words = text.split()
        print(f"Количество слов в файле: {len(words)}")
except FileNotFoundError:
    print("Ошибка: файл text_file.txt не найден.")
