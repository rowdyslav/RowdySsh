from typing import Self

from aiogram.types import User as TgUser
from pydantic import Field

from ._base import Base


class User(Base):
    """Модель пользователя бота"""

    id: int = Field(alias="_id")
    username: str | None = Field(default=None)
    host: str | None = Field(default=None)
    ssh_user: str | None = Field(default=None)
    port: int | None = Field(default=None)
    ssh_password: str | None = Field(default=None)

    @classmethod
    async def get_or_create(cls, tg_user: TgUser) -> Self:
        user = await cls._get(tg_user.id)
        if user:
            await cls._update(user.id, username=tg_user.username)
        else:
            await cls._create(_id=tg_user.id, username=tg_user.username)
        assert user
        return user

    async def update(self, **kwargs: str | int) -> None:
        await User._update(self.id, **kwargs)


User.set_collection("users")
