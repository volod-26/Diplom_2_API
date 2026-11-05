import requests
import allure
from config import LOGIN_ENDPOINT


@allure.feature("Логин пользователя")
class TestLogin:

    @allure.title("Проверка входа с валидными данными")
    def test_login_success(self, create_user):
        email, password, _ = create_user
        response = requests.post(LOGIN_ENDPOINT, json={"email": email, "password": password})
        assert response.status_code == 200
        assert "accessToken" in response.json()

    @allure.title("Проверка входа с неверным паролем")
    def test_login_wrong_password(self, create_user):
        email, password, _ = create_user
        response = requests.post(LOGIN_ENDPOINT, json={"email": email, "password": "wrong_password"})
        assert response.status_code == 401
        assert "incorrect" in response.json()["message"]

    @allure.title("Проверка входа с неверным логином")
    def test_login_wrong_email(self, create_user):
        email, password, _ = create_user
        response = requests.post(LOGIN_ENDPOINT, json={"email": "wrong_email@yandex.ru", "password": password})
        assert response.status_code == 401
        assert "incorrect" in response.json()["message"]

    @allure.title("Проверка входа без поля email")
    def test_login_without_email(self):
        response = requests.post(LOGIN_ENDPOINT, json={"password": "some_password"})
        assert response.status_code == 401
        assert "incorrect" in response.json()["message"]

    @allure.title("Проверка входа без поля password")
    def test_login_without_password(self):
        response = requests.post(LOGIN_ENDPOINT, json={"email": "test@yandex.ru"})
        assert response.status_code == 401
        assert "incorrect" in response.json()["message"]