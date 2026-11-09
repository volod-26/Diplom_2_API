import requests
import pytest
import allure
from config import REGISTER_ENDPOINT, LOGIN_ENDPOINT, USER_ENDPOINT
import helpers


@allure.feature("Регистрация пользователя")
class TestRegistration:

    @allure.title("Проверка создания уникального пользователя")
    def test_create_unique_user(self):
        email = f"{helpers.generate_random_string(10)}@yandex.ru"
        password = helpers.generate_random_string(10)
        name = helpers.generate_random_string(10)
        payload = {"email": email, "password": password, "name": name}

        response = requests.post(REGISTER_ENDPOINT, json=payload)
        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()

    @allure.title("Проверка создания пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, create_user):
        email, password, name = create_user
        payload = {"email": email, "password": password, "name": name}
        response = requests.post(REGISTER_ENDPOINT, json=payload)
        assert response.status_code == 403
        assert response.json()["success"] is False
        assert "already exists" in response.json()["message"]

    @allure.title("Проверка создания пользователя без обязательного поля")
    @pytest.mark.parametrize("field", ["email", "password", "name"])
    def test_create_user_without_field(self, field):
        payload = {
            "email": f"{helpers.generate_random_string(10)}@yandex.ru",
            "password": helpers.generate_random_string(10),
            "name": helpers.generate_random_string(10)
        }
        payload.pop(field)
        response = requests.post(REGISTER_ENDPOINT, json=payload)
        assert response.status_code == 403
        assert response.json()["success"] is False
        assert "required fields" in response.json()["message"]