import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Конфигурация API
DV_API_URL = os.getenv("DV_API_URL")
DV_LOGIN = os.getenv("DV_LOGIN")
DV_PASS = os.getenv("DV_PASS")

# Данные для авторизации
auth_data = {
    "login": DV_LOGIN,
    "password": DV_PASS
}
