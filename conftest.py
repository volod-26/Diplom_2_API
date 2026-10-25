import pytest
import requests
import helpers


BASE_URL = "https://qa-stellarburgers.education-services.ru/api"


@pytest.fixture
def create_user():
    """Фикстура: создает пользователя и удаляет его после теста"""
    user_data = helpers.register_new_user_and_return_login_password()
    yield user_data
    if user_data:
        email = user_data[0]
        password = user_data[1]
        # Получаем токен для удаления
        login_response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        if login_response.status_code == 200:
            token = login_response.json().get("accessToken")
            if token:
                requests.delete(f"{BASE_URL}/auth/user", headers={"Authorization": token})