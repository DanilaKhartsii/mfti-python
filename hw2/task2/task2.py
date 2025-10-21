total = 0

try:
    with open("prices.txt", "r", encoding="utf-8") as file:
        for line in file:
            parts = line.split()
            if len(parts) != 3:
                print(f"Строка пропущена (некорректный формат): {line.strip()}")
                continue

            name, quantity, price = parts
            total += int(quantity) * float(price)

    print(f"Общая стоимость заказа: {total} руб.")
except FileNotFoundError:
    print("Ошибка: файл prices.txt не найден.")
except ValueError:
    print("Ошибка: в файле найдены некорректные данные (не число).")
