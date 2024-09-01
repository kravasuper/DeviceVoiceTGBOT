from bot_config import logger
import nest_asyncio
from bot_config import BOT_TOKEN
from command_handlers import (
    start_command,
    help_command,
    machines_command,
    id_command,
    button,
    go_back
    )
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
import asyncio

# Активируем nest_asyncio для поддержки вложенных циклов событий
nest_asyncio.apply()

async def main() -> None:
    logger.info("Запуск бота...")

    # Создание и запуск приложения
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))

    # Обработчик кнопки back
    application.add_handler(CallbackQueryHandler(go_back, pattern="go_back"))

    # Регистрация обработчика команды /id
    application.add_handler(CommandHandler("id", id_command))

    # Регистрация обработчика команды /machines
    application.add_handler(CommandHandler("machines", machines_command))

    application.add_handler(CallbackQueryHandler(button))

    # Запуск бота с использованием polling
    await application.run_polling()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"Произошла ошибка при запуске бота: {str(e)}")
