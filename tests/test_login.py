import requests
import helpers


BASE_URL = "https://qa-stellarburgers.education-services.ru/api"


class TestLogin:
    """Тесты для ручки «Логин пользователя»"""

    def test_login_success(self, create_user):
        """Вход под существующим пользователем"""
        email, password, name = create_user

        payload = {
            "email": email,
            "password": password
        }

        response = requests.post(f"{BASE_URL}/auth/login", json=payload)

        assert response.status_code == 200
        assert response.json()["success"] is True
        assert "accessToken" in response.json()
        assert "refreshToken" in response.json()

    def test_login_wrong_password(self, create_user):
        """Вход с неверным паролем"""
        email, password, name = create_user

        payload = {
            "email": email,
            "password": "wrong_password"
        }

        response = requests.post(f"{BASE_URL}/auth/login", json=payload)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert "incorrect" in response.json()["message"]

    def test_login_wrong_email(self, create_user):
        """Вход с неверным логином (email)"""
        email, password, name = create_user

        payload = {
            "email": "wrong_email@yandex.ru",
            "password": password
        }

        response = requests.post(f"{BASE_URL}/auth/login", json=payload)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert "incorrect" in response.json()["message"]

    def test_login_without_email(self):
        """Вход без поля email"""
        payload = {
            "password": "some_password"
        }

        response = requests.post(f"{BASE_URL}/auth/login", json=payload)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert "incorrect" in response.json()["message"]

    def test_login_without_password(self):
        """Вход без поля password"""
        payload = {
            "email": "test@yandex.ru"
        }

        response = requests.post(f"{BASE_URL}/auth/login", json=payload)

        assert response.status_code == 401
        assert response.json()["success"] is False
        assert "incorrect" in response.json()["message"]