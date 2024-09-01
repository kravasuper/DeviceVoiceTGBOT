from auth import get_authorization_token
import httpx
import logging
from config import DV_API_URL
from datetime import datetime

logger = logging.getLogger(__name__)

# Глобальная переменная для токена
authorization_token = get_authorization_token()

async def make_request(url: str, params: dict = None):
    global authorization_token

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers={"Authorization": authorization_token}, params=params)
            response.raise_for_status()
            return response.json()

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:  # Проверка на истекший токен
                logger.warning("Токен истек. Получение нового токена...")
                authorization_token = get_authorization_token()  # Получаем новый токен

                # Повторный запрос с новым токеном
                response = await client.get(url, headers={"Authorization": authorization_token}, params=params)
                response.raise_for_status()
                return response.json()
            else:
                logger.error(f"Ошибка при запросе: {str(e)}")
                raise Exception(f"Ошибка при запросе: {str(e)}")

        except httpx.RequestError as e:
            logger.error(f"Ошибка сети: {str(e)}")
            raise Exception(f"Ошибка сети: {str(e)}")


async def get_machines():
    """
    Асинхронное получение списка машин.
    :return: Список машин
    """
    url = f"{DV_API_URL}/monitoring/machines"
    return await make_request(url)


async def get_events_id(machine_id: int):
    """
    Асинхронное получение данных по id машинки.
    """
    today = datetime.now()
    start_of_day = today.replace(hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%S")
    end_of_day = today.replace(hour=23, minute=59, second=59).strftime("%Y-%m-%dT%H:%M:%S")

    url = f"{DV_API_URL}/machines/events"
    params = {
        "machines": machine_id,
        "start": 0,
        "limit": 4,
        "from": start_of_day,
        "to": end_of_day
    }
    return await make_request(url, params)
