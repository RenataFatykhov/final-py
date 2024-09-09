import requests

BASE_URL = "https://www.aviasales.ru"

# Получение временного email через API 1secmail
def get_temp_email():
    response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
    email = response.json()[0]
    print(f"Используем временный email: {email}")
    return email

# Генерация временной почты для тестов
USER_DATA = {
    "username": get_temp_email(),       # Временный email
    "password": "TemporaryPassword123!"  # Временный пароль для тестов
}

# Токен будет получен динамически
TOKEN = None