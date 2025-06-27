import asyncio
import logging
from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.client.default import DefaultBotProperties

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def webapp_builder() -> InlineKeyboardBuilder:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="🍊 Играть в KYBNK Clicker",
        web_app=WebAppInfo(url="https://api.cloudflare.com/client/v4/accounts/cec8d068d1d126954dfc583292897621/tokens/verify")
    )
    return builder.as_markup()
    

router = Router()


@router.message(CommandStart())
async def start_command(message: Message) -> None:
    logger.info(f"User {message.from_user.id} started the bot")
    try:
        await message.reply(
            "Добро пожаловать в KYBNK Clicker!\n\n"
            "Нажмите кнопку ниже, чтобы начать игру:",
            reply_markup=webapp_builder()
        )
        logger.info("Start message sent successfully")
    except Exception as e:
        logger.error(f"Error sending start message: {str(e)}")


async def main() -> None:
    logger.info("Starting bot...")

    # Инициализация бота с правильными параметрами
    bot = Bot(
        token='8131382951:AAEYbYjhBod6_iETzK-qGeiKvhDnVnjy10w',
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # Инициализация диспетчера с роутером
    dp = Dispatcher()
    dp.include_router(router)

    try:
        # Удаляем вебхук и запускаем поллинг
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Webhook deleted")

        await dp.start_polling(bot)
        logger.info("Polling started")
    except Exception as e:
        logger.critical(f"Bot failed: {str(e)}")
    finally:
        await bot.session.close()
        logger.info("Bot session closed")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.critical(f"Unexpected error: {str(e)}")