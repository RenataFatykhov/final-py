import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
from config import BASE_URL, USER_DATA

@pytest.fixture
def setup_browser():
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@allure.step("Открытие главной страницы")
def open_main_page(driver):
    driver.get(BASE_URL)

@allure.step("Авторизация пользователя")
def login(driver, username, password):
    driver.find_element(By.ID, "login_button").click()
    driver.find_element(By.ID, "username").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "submit_login").click()

    # Ожидание успешного входа
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "user-profile"))
    )

@allure.step("Поиск билетов по городам")
def search_tickets(driver, from_city, to_city):
    driver.find_element(By.ID, "origin").send_keys(from_city)
    driver.find_element(By.ID, "destination").send_keys(to_city)
    driver.find_element(By.ID, "search_button").click()

@allure.step("Ожидание загрузки результатов поиска")
def wait_for_search_results(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "search-results"))
    )

@allure.step("Выбор первого доступного билета")
def select_first_ticket(driver):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".ticket-item"))
    ).click()

@pytest.mark.ui
def test_search_tickets(setup_browser):
    driver = setup_browser
    open_main_page(driver)
    search_tickets(driver, "Москва", "Сочи")
    
    wait_for_search_results(driver)
    assert "Результаты поиска" in driver.page_source

@pytest.mark.ui
def test_select_ticket_with_login(setup_browser):
    driver = setup_browser
    open_main_page(driver)
    
    # Логин перед бронированием
    login(driver, USER_DATA["username"], USER_DATA["password"])
    
    search_tickets(driver, "Москва", "Сочи")
    
    wait_for_search_results(driver)
    select_first_ticket(driver)
    
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "booking-form"))
    )
    assert "Бронирование" in driver.page_source
