import asyncio

import fabric
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.filters.command import CommandObject
from aiogram.types import Message
from environs import Env
from icecream import ic
from paramiko.ssh_exception import SSHException

from database.models import User

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
    tg_user = message.from_user
    if not tg_user:
        return
    db_user = await User.get_or_create(tg_user)

    host, ssh_password = db_user.host, db_user.ssh_password
    if not all((host, ssh_password)):
        args = command.args
        if not args:
            await message.answer("Формат: /connect <айпи> <юзер> <порт> <пароль>")
            return
        host, ssh_user, port, ssh_password = args.split()
        await db_user.update(
            host=host, ssh_user=ssh_user, port=int(port), ssh_password=ssh_password
        )
    ssh_user = db_user.ssh_user if db_user.ssh_user else "root"
    port = db_user.port if db_user.port else 22

    assert host
    assert ssh_password

    await message.answer("Подключение к машине...")
    conn = fabric.Connection(
        host, ssh_user, port, connect_kwargs={"password": ssh_password}
    )
    try:
        result = conn.run("uname -s", hide=True)
    except SSHException as e:
        match str(e):
            case "Error reading SSH protocol banner":
                await message.answer(
                    "Ошибка SSH protocol banner! Скорее всего машина отключена"
                )
            case _:
                await message.answer("Неизвестная ошибка SSHException!")
                raise e
        return
    msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
    await message.answer(msg.format(result))


async def main():
    bot = Bot(TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
