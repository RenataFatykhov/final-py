import requests
import pytest
import allure
from config import BASE_URL, USER_DATA

@allure.step("Получение токена авторизации")
def get_auth_token():
    response = requests.post(f"{BASE_URL}/api/auth/login", json={
        "username": USER_DATA["username"],
        "password": USER_DATA["password"]
    })
    assert response.status_code == 200
    return response.json()["token"]

@pytest.fixture(scope="session")
def auth_token():
    token = get_auth_token()
    return token

@allure.step("Отправка запроса на поиск билетов с авторизацией")
def search_flights(from_city, to_city, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/flights", params={"from": from_city, "to": to_city}, headers=headers)
    return response

@allure.step("Отправка запроса на бронирование билета с авторизацией")
def book_ticket(ticket_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/api/book", json={"ticket_id": ticket_id}, headers=headers)
    return response

@allure.step("Получение информации о билете с авторизацией")
def get_ticket_info(ticket_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/tickets/{ticket_id}", headers=headers)
    return response

@allure.step("Отправка запроса на отмену бронирования с авторизацией")
def cancel_booking(booking_id, token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(f"{BASE_URL}/api/cancel", json={"booking_id": booking_id}, headers=headers)
    return response

@allure.step("Проверка доступности API с авторизацией")
def check_api_status(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/status", headers=headers)
    return response

# Тесты
@pytest.mark.api
def test_search_flights(auth_token):
    response = search_flights("Moscow", "Sochi", auth_token)
    assert response.status_code == 200
    assert "flights" in response.json()
    
    # Получаем ID первого билета для последующих тестов
    ticket_id = response.json()["flights"][0]["id"]
    return ticket_id

@pytest.mark.api
def test_book_ticket(auth_token):
    # Используем ticket_id, полученный в предыдущем тесте
    ticket_id = test_search_flights(auth_token)
    
    response = book_ticket(ticket_id, auth_token)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    
    # Получаем ID бронирования для последующих тестов
    booking_id = response.json()["booking_id"]
    return booking_id

@pytest.mark.api
def test_get_ticket_info(auth_token):
    # Используем ticket_id из поиска билетов
    ticket_id = test_search_flights(auth_token)
    
    response = get_ticket_info(ticket_id, auth_token)
    assert response.status_code == 200
    assert "ticket" in response.json()

@pytest.mark.api
def test_cancel_booking(auth_token):
    # Используем booking_id из бронирования билета
    booking_id = test_book_ticket(auth_token)
    
    response = cancel_booking(booking_id, auth_token)
    assert response.status_code == 200
    assert response.json()["status"] == "canceled"

@pytest.mark.api
def test_check_api_status(auth_token):
    response = check_api_status(auth_token)
    assert response.status_code == 200
    assert response.json()["status"] == "available"
