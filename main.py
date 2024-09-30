import asyncio

from aiogram import Bot, Dispatcher
from environs import Env

from commands import router as commands_router

dp = Dispatcher()
dp.include_routers(commands_router)

env = Env()
env.read_env()


async def main():
    bot = Bot(env.str("TOKEN"))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
