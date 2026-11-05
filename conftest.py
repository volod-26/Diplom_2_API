import pytest
import requests
import helpers
from config import LOGIN_ENDPOINT, USER_ENDPOINT


@pytest.fixture
def create_user():
    """Фикстура: создает пользователя и удаляет его после теста"""
    user_data = helpers.register_new_user_and_return_login_password()
    yield user_data
    if user_data:
        email, password, _ = user_data
        login_response = requests.post(LOGIN_ENDPOINT, json={"email": email, "password": password})
        if login_response.status_code == 200:
            token = login_response.json().get("accessToken")
            if token:
                requests.delete(USER_ENDPOINT, headers={"Authorization": token})