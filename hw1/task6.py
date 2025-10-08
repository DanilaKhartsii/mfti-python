try:
    import math
    x = float(input("Введите число для вычисления квадратного корня: "))
    result = math.sqrt(x)
except ImportError:
    print("Ошибка: не удалось импортировать модуль math.")
except ValueError:
    print("Ошибка: нельзя вычислить квадратный корень из отрицательного числа.")
else:
    print(f"Квадратный корень из {x} равен {result}")
