from typing import Self

from pydantic import Field

from .base import Base


class User(Base):
    id: int = Field(alias="_id")
    username: str | None = Field(default=None)
    host: str | None = Field(default=None)
    ssh_user: str | None = Field(default=None)
    port: int | None = Field(default=None)
    ssh_password: str | None = Field(default=None)

    @classmethod
    async def get_or_create(cls, id: int, username: str | None) -> Self:
        user = await cls._get(id)
        user = (
            await cls._update(user.id, username=username)
            if user
            else await cls._create(_id=id, username=username)
        )
        assert user
        return user

    async def update(self, **kwargs: str | int) -> None:
        await User._update(self.id, **kwargs)


User.set_collection("users")
