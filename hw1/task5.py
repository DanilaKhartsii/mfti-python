try:
    s = input("Введите число: ")
    num = float(s)
except ValueError:
    print("Ошибка: введённая строка не может быть преобразована в число.")
else:
    print(f"Преобразованное число: {num}")
