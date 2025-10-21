try:
    with open("source.txt", "r", encoding="utf-8") as source:
        content = source.read()

    with open("destination.txt", "w", encoding="utf-8") as destination:
        destination.write(content)

    print("Содержимое успешно скопировано в destination.txt.")
except FileNotFoundError:
    print("Ошибка: исходный файл не найден.")
except IOError:
    print("Ошибка при работе с файлами.")
