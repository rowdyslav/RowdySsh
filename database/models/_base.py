from typing import Self

from motor.motor_tornado import MotorCollection
from pydantic import BaseModel

from ..loader import db


class Base(BaseModel):
    _collection: MotorCollection = None  # type: ignore

    @classmethod
    async def _create(cls, **kwargs) -> Self:
        obj = cls(**kwargs).model_dump(by_alias=True)
        await cls._collection.insert_one(obj)
        return cls(**obj)

    @classmethod
    async def _get(cls, id: int) -> Self | None:
        obj = await cls._collection.find_one({"_id": id})
        return cls(**obj) if obj else None

    @classmethod
    async def _update(cls, id: int, **kwargs: str | int | None) -> None:
        await cls._collection.find_one_and_update({"_id": id}, {"$set": kwargs})

    @classmethod
    async def _delete(cls, id: int) -> None:
        await cls._collection.find_one_and_delete({"_id": id})

    @classmethod
    def set_collection(cls, collection: str) -> None:
        cls._collection = db[collection]
