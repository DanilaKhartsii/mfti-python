import requests

API_KEY = "f7d8632a2beb99436593721aad751bf9"
city = input("Введите название города: ")

URL = "https://api.openweathermap.org/data/2.5/weather"
params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric",
    "lang": "ru",
}

response = requests.get(url=URL, params=params)

if response.status_code == 200:
    data = response.json()
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    print(f"Погода в {city}: {temp}C, {description}")
else:
    print("Ошибка запроса: ", response.status_code)