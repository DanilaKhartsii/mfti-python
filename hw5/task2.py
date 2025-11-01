import threading
import time

def print_numbers(thread_name):
    for i in range(1, 11):
        print(f"{thread_name}: {i}")
        time.sleep(1)

threads = []

for num in range(3):
    t = threading.Thread(target=print_numbers, args=(f"Поток {num + 1}",))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("Все потоки завершили работу.")