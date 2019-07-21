from typing import Union
from uuid import uuid4

from sqlalchemy import Column, String, Text

from app import wrapper


class Inventory(wrapper.Base):
    __tablename__ = "Inventory"

    element_uuid: Union[Column, str] = Column(String(36), primary_key=True, unique=True)
    element_name: Union[Column, str] = Column(Text())
    related_ms: Union[Column, str] = Column(Text())
    owner: Union[Column, str] = Column(String(36))

    @property
    def serialize(self) -> dict:
        _: str = self.element_uuid
        d: dict = self.__dict__.copy()

        del d["_sa_instance_state"]

        return d

    @staticmethod
    def create(name: str, owner: str, related_service: str) -> 'Inventory':
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
