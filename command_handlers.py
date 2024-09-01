from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from machines_views import get_machines, get_events_id
import httpx
from bot_config import logger, ADMIN_ID


async def start_command(update: Update, context: CallbackContext) -> None:
    """
    Обработчик команды /start.
    Приветствует пользователя.
    """
    logger.info("Получена команда /start")
    await update.message.reply_text('Привет! Это бот для взаимодействия с вашим API.')


async def id_command(update: Update, context: CallbackContext) -> None:
    """
    Обработчик команды /id.
    Возвращаeт ID пользователя.
    """
    user_id = update.message.from_user.id
    await update.message.reply_text(f"Ваш ID: {user_id}")


async def help_command(update: Update, context: CallbackContext) -> None:
    """
    Обработчик команды /help.
    Предоставляет информацию о боте.
    """
    logger.info("Получена команда /help")
    await update.message.reply_text("Это бот для взаимодействия с API. Используйте команды для взаимодействия.")


async def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    try:
        # Асинхронное получение списка событий по ID машины
        response = await get_events_id(int(query.data))  # Предполагается, что query.data содержит ID машины
        # Извлечение данных о событиях
        machine_events = response.get("items", [])
        if not machine_events:
            await query.edit_message_text("Список событий пуст.")
            return
        # Формирование сообщения с событиями
        event_messages = []
        for event in machine_events:
            # Используем статус для отображения галочки или крестика
            status_icon = (
                "✔️" if event['type'] == "SOLVED" else
                "❓" if event['type'] == "UNKNOWN" else
                "🔄" if event['type'] == "ACTIVE" else
                "ℹ️" if event['type'] == "INFO" else
                "❌"  # По умолчанию, если статус неизвестен
            )
            event_message = (
                f"{status_icon} {event['name']}\n"
                f"Код: {event['code']}\n"
                f"Описание: {event['description']}\n"
                f"Время: {event['receive_server_time']}\n"
                # f"Машина: {event['machine']['title']}\n"
                #f"Адрес: {event['location']['extra'][0]['value']}\n"
                f"---\n"
            )
            event_messages.append(event_message)
        # Объединение всех сообщений в одно
        message_text = "\n".join(event_messages)
        # Добавлние кнопки "Назад"
        keyboard = [[InlineKeyboardButton("Назад", callback_data="go_back")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Отправка сообщения пользователю с кнопкой "Назад"
        await query.edit_message_text(f"Список событий  {machine_events[0]['machine']['title']}:\n\n{message_text}",
                                      reply_markup=reply_markup)
    except httpx.RequestError as e:
        await query.edit_message_text(f"Ошибка при получении списка событий: {str(e)}")
    except Exception as e:
        await query.edit_message_text(f"Произошла непредвиденная ошибка: {str(e)}")


async def go_back(update: Update, context: CallbackContext) -> None:
    """Обработчик кнопки 'Назад'."""
    query = update.callback_query
    await query.answer()
    # Здесь добавьте код, который будет выполняться при возврате
    # Например, можно отправить стартовое сообщение или другую клавиатуру
    # await query.edit_message_text("Вы вернулись назад. Выберите дальнейшие действия. /machines")
    # Вызываем функцию machines_command, передавая оригинальный объект update
    await machines_command(update, context)


from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import httpx


async def machines_command(update: Update, context: CallbackContext) -> None:
    """
    Обработчик команды /machines.
    Запрашивает список машин и отправляет его пользователю.
    """
    query = update.callback_query
    if query:
        await query.answer()

    try:
        # Определение объекта message, который может быть как update.message, так и update.callback_query.message
        message = update.message if update.message else update.callback_query.message

        # Асинхронное получение списка машин
        response = await get_machines()  # Используйте нужные параметры

        # Извлечение данных о машинах
        machine_states = response.get("machine_states", {})
        if not machine_states:
            await message.reply_text("Список машин пуст.")
            return

        # Создаем текст сообщения
        keyboard = []
        html_text = "/machines\n"
        html_text += "<pre>"
        for state in ["error", "bad", "good"]:
            for machine in machine_states.get(state, []):
                status_icon = (
                    "✔️" if machine["status"] == "OK" else
                    "❌" if machine["status"] == "OFFLINE" else
                    "⚠️" if machine["status"] == "WARNING" else
                    "❓" if machine["status"] == "UNKNOWN" else
                    "🆘"
                )

                gsm_time = machine["gsm_time"]
                time_part = gsm_time.split(" ")[1]

                gsm_status = f"📶 {machine['gsm_level']}% [{time_part}]"
                time_err = machine.get("timeErr", "")
                alarm_time = f"⏰ {time_err}" if time_err else ""

                # Форматируем текст для таблицы
                html_text += f"{status_icon} {machine['name']:<13} {gsm_status:<5} {alarm_time}\n"

                # Добавляем кнопки в клавиатуру
                keyboard.append([
                    InlineKeyboardButton(f"{machine['name']}", callback_data=str(machine['id']))
                ])

        html_text += "</pre>"

        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправляем сообщение с кнопками
        await message.reply_text(html_text, parse_mode="HTML", reply_markup=reply_markup)

    except httpx.RequestError as e:
        if message:
            await message.reply_text(f"Ошибка при получении списка машин: {str(e)}")
    except Exception as e:
        if message:
            await message.reply_text(f"Произошла непредвиденная ошибка: {str(e)}")


