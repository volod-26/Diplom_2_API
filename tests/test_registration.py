import requests
import helpers


BASE_URL = "https://qa-stellarburgers.education-services.ru/api"


class TestRegistration:
    """Тесты для ручки «Создание пользователя»"""

    def test_create_unique_user(self, create_user):
        """Проверка создания уникального пользователя"""
        user_data = create_user
        assert len(user_data) == 3
        assert user_data[0] != ""
        assert "@" in user_data[0]

    def test_create_existing_user(self, create_user):
        """Проверка создания пользователя, который уже зарегистрирован"""
        user_data = create_user
        email, password, name = user_data

        payload = {
            "email": email,
            "password": password,
            "name": name
        }

        response = requests.post(f"{BASE_URL}/auth/register", json=payload)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert "already exists" in response.json()["message"]

    def test_create_user_without_email(self):
        """Проверка создания пользователя без обязательного поля (email)"""
        payload = {
            "password": helpers.generate_random_string(10),
            "name": helpers.generate_random_string(10)
        }

        response = requests.post(f"{BASE_URL}/auth/register", json=payload)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert "required fields" in response.json()["message"]

    def test_create_user_without_password(self):
        """Проверка создания пользователя без обязательного поля (password)"""
        payload = {
            "email": f"{helpers.generate_random_string(10)}@yandex.ru",
            "name": helpers.generate_random_string(10)
        }

        response = requests.post(f"{BASE_URL}/auth/register", json=payload)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert "required fields" in response.json()["message"]

    def test_create_user_without_name(self):
        """Проверка создания пользователя без обязательного поля (name)"""
        payload = {
            "email": f"{helpers.generate_random_string(10)}@yandex.ru",
            "password": helpers.generate_random_string(10)
        }

        response = requests.post(f"{BASE_URL}/auth/register", json=payload)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert "required fields" in response.json()["message"]