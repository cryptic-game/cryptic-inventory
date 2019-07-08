from sqlalchemy import Column, String, Text
from typing import Union
from uuid import uuid4
from vars import config as game_info
from app import wrapper


class Inventory(wrapper.Base):
    __tablename__ = "Inventory"

    element_uuid: Union[Column, str] = Column(String(36), unique=True)
    element_name: Union[Column, str] = Column(Text())
    related_ms: Union[Column, str] = Column(Text())
    owner: Union[Column, str] = Column(String(36))

    @property
    def serialize(self) -> dict:
        _: str = self.source_uuid
        d = self.__dict__

        del d["_sa_instance_state"]
        d["time_stamp"] = str(d["time_stamp"])

        return d

    @staticmethod
    def create(name: str, owner: str, related_service: str) -> Union[None, "Inventory"]:

        if name in game_info["items"].key():
            element_uuid: str = str(uuid4())

            inventory: Inventory = Inventory(
                owner=owner,
                element_name=name,
                element_uuid=element_uuid,
                related_ms=related_service,
            )

            wrapper.session.add(inventory)
            wrapper.session.commit()

            return inventory
