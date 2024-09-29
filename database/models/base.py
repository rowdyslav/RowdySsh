from motor.motor_tornado import MotorCollection
from pydantic import BaseModel

from ..loader import db


class Base(BaseModel):
    _collection: MotorCollection = None  # type: ignore

    @classmethod
    async def _get(cls, id: int):
        obj = await cls._collection.find_one({"_id": id})
        return cls(**obj) if obj else None

    @classmethod
    async def _update(cls, id: int, **kwargs: str | int | None):
        await cls._collection.find_one_and_update({"_id": id}, {"$set": kwargs})
        return await cls._get(id)

    @classmethod
    async def _create(cls, **kwargs):
        if "_id" not in kwargs:
            kwargs["_id"] = int()
        obj = cls(**kwargs)
        obj = await cls._collection.insert_one(obj.model_dump(by_alias=True))
        return await cls._get(obj.inserted_id)

    @classmethod
    async def _delete(cls, id: int):
        await cls._collection.find_one_and_delete({"_id": id})
        return True

    @classmethod
    def set_collection(cls, collection: str):
        cls._collection = db[collection]
