import requests

URL = "https://jsonplaceholder.typicode.com/posts"
new_post = {
    "title": "Пост с обработкой ошибок",
    "body": "Тело поста",
    "userId": 1000
}

try:
    response = requests.post(URL, json=new_post)

    if response.status_code in (200, 201):
        print("Успех: ", response.json())
    elif response.status_code == 400:
        print("Ошибка 400 - неверный запрос.")
    elif response.status_code == 404:
        print("Ошибка 404 - ресурс не найден.")
    else:
        print(f"Неизвестная ошибка: {response.status_code}")
        print("Ответ сервера: ", response.text)

except requests.exceptions.MissingSchema:
    print("Неверный URL")
except requests.exceptions.ConnectionError:
    print("Ошибка соединения: сервер недоступен или URL неверный")
except requests.exceptions.Timeout:
    print("Превышено время ожидания ответа.")
except Exception as e:
    print("Неизвестная ошибка: ", type(e).__name__, "-", str(e))