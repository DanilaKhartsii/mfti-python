import requests

URL = "https://jsonplaceholder.typicode.com/posts"

response = requests.get(URL)

if response.status_code == 200:
    posts = response.json()
    for post in posts[:5]:
        print(f"ID: {post['id']}")
        print(f"Заголовок: {post['title']}")
        print(f"Тело: {post['body']}")
else:
    print("Ошибка:", response.status_code)
