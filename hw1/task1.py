try:
    a = float(input("Введите первое число: "))
    b = float(input("Введите второе число: "))
    result = a / b
except ZeroDivisionError:
    print("Ошибка: деление на ноль невозможно.")
else:
    print(f"Результат: {result}")