import asyncio
import logging
import sys
from config import bot_token
from aiogram import Bot, Dispatcher
from routers import message_router, inline_router


dp = Dispatcher()



async def main() -> None:
    bot = Bot(token=bot_token)
    dp.include_routers(message_router.router, inline_router.router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())