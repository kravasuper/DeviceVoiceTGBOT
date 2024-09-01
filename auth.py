import requests
from config import DV_API_URL, auth_data

def get_authorization_token():
    """
    Получение токена авторизации.
    Возвращает токен или вызывает исключение при ошибке.
    """
    try:
        response = requests.post(f"{DV_API_URL}/authorizations/login", json=auth_data)
        response.raise_for_status()
        return response.json().get("token")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ошибка авторизации: {e}")
