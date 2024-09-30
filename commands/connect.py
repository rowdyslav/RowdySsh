import fabric
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from icecream import ic
from paramiko.ssh_exception import SSHException

from database.models import User
from routers import commands_router as router


@router.message(Command("connect"))
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
        host,
        ssh_user,
        port,
        connect_kwargs={"password": ssh_password, "banner_timeout": 60},
    )

    try:
        conn.open()
    except (SSHException, TimeoutError, ConnectionResetError) as e:
        if "Error reading SSH protocol banner" in str(e):
            await message.answer(
                "Ошибка SSH protocol banner! Скорее всего машина отключена"
            )
        else:
            await message.answer("Неизвестная ошибка подключения!")
            ic(e)
        return

    result = conn.run("uname -s", hide=True)
    msg = "Ran {0.command!r} on {0.connection.host}, got stdout:\n{0.stdout}"
    await message.answer(msg.format(result))
