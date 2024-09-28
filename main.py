import asyncio

import fabric
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.filters.command import CommandObject
from aiogram.types import Message
from environs import Env

dp = Dispatcher()

env = Env()
env.read_env()

TOKEN = env.str("TOKEN")


@dp.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Чтобы начать работу с ботом настройте подключение к вашей машине /connect"
    )


@dp.message(Command("connect"))
async def connect(message: Message, command: CommandObject):
    args = command.args
    if not args:
        await message.answer("Формат: /connect <айпи> <юзер> <порт> <пароль>")
        return
    host, user, port, password = args.split()
    result = fabric.Connection(
        host, user, port, connect_kwargs={"password": password}
    ).run("uname -s", hide=True)

    msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
    await message.answer(msg.format(result))


async def main():
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
