from aiogram.filters import CommandStart
from aiogram.types import Message

from routers import command_router as router


@router.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Чтобы начать работу с ботом настройте подключение к вашей машине /connect"
    )
