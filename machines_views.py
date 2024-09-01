from auth import get_authorization_token
import httpx
import logging
from config import DV_API_URL
from datetime import datetime

logger = logging.getLogger(__name__)

# Получение токена авторизации
authorization_token = get_authorization_token()

# async def get_machines(page: int = 1, page_size: int = 10):
async def get_machines():
    """
    Асинхронное получение списка машин.
    :return: Список машин
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{DV_API_URL}/monitoring/machines",
                headers={"Authorization": authorization_token},
                # params={"page": page, "page_size": page_size}
            )
        response.raise_for_status()
        logger.debug(response.json())
        return response.json()
    except httpx.RequestError as e:
        logger.error(f"Ошибка при получении списка машин: {str(e)}")
        raise Exception(f"Ошибка при получении списка машин: {str(e)}")

async def get_events_id(machine_id: int):
    """
    Асинхронное получение данных по id машинки.
    """
    # Получаем текущую дату
    today = datetime.now()

    # Форматируем начало и конец дня
    start_of_day = today.replace(hour=0, minute=0, second=0).strftime("%Y-%m-%dT%H:%M:%S")
    end_of_day = today.replace(hour=23, minute=59, second=59).strftime("%Y-%m-%dT%H:%M:%S")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{DV_API_URL}/machines/events",
                headers={"Authorization": authorization_token},
                params={
                    "machines": machine_id,
                    "start": 0,
                    "limit": 4,
                    "from": start_of_day,
                    "to": end_of_day
                }
            )
        response.raise_for_status()
        logger.debug(response.json())
        return response.json()
    except httpx.RequestError as e:
        logger.error(f"Ошибка при получении списка машин: {str(e)}")
        raise Exception(f"Ошибка при получении списка машин: {str(e)}")