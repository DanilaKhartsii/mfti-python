my_list = ['яблоко', 'банан', 'вишня', 'груша']

try:
    index = int(input("Введите индекс элемента: "))
    print(f"Элемент: {my_list[index]}")
except ValueError:
    print("Ошибка: нужно вводить число.")
except IndexError:
    print("Ошибка: индекс выходит за пределы списка.")
