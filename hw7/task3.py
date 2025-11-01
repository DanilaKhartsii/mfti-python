import requests

URL = "https://jsonplaceholder.typicode.com/posts"
new_post = {
    "title": "Мой новый пост",
    "body": "Тело поста",
    "userId": 1,
}

response = requests.post(URL, json=new_post)

if response.status_code == 201:
    post = response.json()
    print("Пост успешно создан")
    print("ID: ", post["id"])
    print("Содержимое: ", post)
else:
    print("Ошибка:", response.status_code)