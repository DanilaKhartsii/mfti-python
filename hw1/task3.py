class EvenNumberError(Exception):
    pass

class NegativeNumberError(Exception):
    pass


def sum_list(numbers):
    total = 0
    for n in numbers:
        if n < 0:
            raise NegativeNumberError("Список содержит отрицательное число.")
        if n % 2 == 0:
            raise EvenNumberError("Список содержит чётное число.")
        total += n
    return total


try:
    nums = [1, 3, 5, 7]
    result = sum_list(nums)
except NegativeNumberError as err:
    print("Ошибка:", err)
except EvenNumberError as err:
    print("Ошибка:", err)
else:
    print("Сумма:", result)
