import threading

def squares():
    for i in range(1, 11):
        print(f"Квадрат { i } = { i**2 }")

def cubes():
    for i in range(1, 11):
        print(f"Куб { i } = { i**3 }")

t1 = threading.Thread(target=squares)
t2 = threading.Thread(target=cubes)

t1.start()
t2.start()

t1.join()
t2.join()

print("Вычисления завершены")