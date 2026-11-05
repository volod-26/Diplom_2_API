import requests
import pytest
import allure
from config import ORDERS_ENDPOINT, INGREDIENTS_ENDPOINT, LOGIN_ENDPOINT


@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.step("Получить токен авторизации")
    def get_token(self, email, password):
        response = requests.post(LOGIN_ENDPOINT, json={"email": email, "password": password})
        return response.json()["accessToken"]

    @allure.step("Получить ID ингредиента")
    def get_ingredient_id(self):
        response = requests.get(INGREDIENTS_ENDPOINT)
        return response.json()["data"][0]["_id"]

    @allure.title("Проверка создания заказа с авторизацией и с ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, create_user):
        email, password, _ = create_user
        token = self.get_token(email, password)
        ingredient_id = self.get_ingredient_id()
        payload = {"ingredients": [ingredient_id]}
        response = requests.post(ORDERS_ENDPOINT, json=payload, headers={"Authorization": token})
        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Проверка создания заказа без авторизации")
    def test_create_order_without_auth(self):
        payload = {"ingredients": ["609646e4dc916e00276b2870"]}
        response = requests.post(ORDERS_ENDPOINT, json=payload)
        assert response.status_code == 400

    @allure.title("Проверка создания заказа без ингредиентов")
    def test_create_order_without_ingredients(self, create_user):
        email, password, _ = create_user
        token = self.get_token(email, password)
        payload = {"ingredients": []}
        response = requests.post(ORDERS_ENDPOINT, json=payload, headers={"Authorization": token})
        assert response.status_code == 400
        assert "Ingredient ids must be provided" in response.text

    @allure.title("Проверка создания заказа с неверным хешем ингредиента")
    def test_create_order_with_invalid_ingredient_hash(self, create_user):
        email, password, _ = create_user
        token = self.get_token(email, password)
        payload = {"ingredients": ["invalid_hash_123"]}
        response = requests.post(ORDERS_ENDPOINT, json=payload, headers={"Authorization": token})
        assert response.status_code == 500