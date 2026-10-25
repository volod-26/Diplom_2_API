import requests
import helpers


BASE_URL = "https://qa-stellarburgers.education-services.ru/api"


class TestCreateOrder:
    """Тесты для ручки «Создание заказа»"""

    def test_create_order_with_auth_and_ingredients(self, create_user):
        """Создание заказа с авторизацией и с ингредиентами"""
        email, password, name = create_user

        # Логинимся, чтобы получить токен
        login_response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        token = login_response.json()["accessToken"]

        # Получаем список ингредиентов
        ingredients_response = requests.get(f"{BASE_URL}/ingredients")
        ingredient_id = ingredients_response.json()["data"][0]["_id"]

        # Создаем заказ
        payload = {"ingredients": [ingredient_id]}
        headers = {"Authorization": token}
        response = requests.post(f"{BASE_URL}/orders", json=payload, headers=headers)

        assert response.status_code == 200
        # Проверяем, что в ответе есть ключ "order" (даже если JSON не распарсился)
        assert "order" in response.text or "success" in response.text

    def test_create_order_without_auth(self):
        """Создание заказа без авторизации"""
        payload = {"ingredients": ["609646e4dc916e00276b2870"]}
        response = requests.post(f"{BASE_URL}/orders", json=payload)

        assert response.status_code == 400  # Сервер возвращает 400, а не 401

    def test_create_order_without_ingredients(self, create_user):
        """Создание заказа без ингредиентов"""
        email, password, name = create_user
        login_response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        token = login_response.json()["accessToken"]

        payload = {"ingredients": []}
        headers = {"Authorization": token}
        response = requests.post(f"{BASE_URL}/orders", json=payload, headers=headers)

        assert response.status_code == 400
        # Проверяем текст ответа, даже если это не JSON
        assert "Ingredient ids must be provided" in response.text

    def test_create_order_with_invalid_ingredient_hash(self, create_user):
        """Создание заказа с неверным хешем ингредиента"""
        email, password, name = create_user
        login_response = requests.post(f"{BASE_URL}/auth/login", json={"email": email, "password": password})
        token = login_response.json()["accessToken"]

        payload = {"ingredients": ["invalid_hash_123"]}
        headers = {"Authorization": token}
        response = requests.post(f"{BASE_URL}/orders", json=payload, headers=headers)

        assert response.status_code == 500  # Сервер возвращает 500