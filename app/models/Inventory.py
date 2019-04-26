from objects import *
from sqlalchemy import Column, Integer, String, Boolean, Text
from typing import Dict, Any, Union
from uuid import uuid4


class Inventory(Base):
    __tablename__ = "Inventory"

    element_uuid: Union[Column, str] = Column(String(36), unique=True)
    element_name: Union[Column, str] = Column(Text())
    related_ms: Union[Column, str] = Column(Text())
    owner: Union[Column, str] = Column(String(36))

    @staticmethod
    def create(name: str, owner: str, related_service: str) -> None:
        element_uuid: str = str(uuid4())

        inventory: Inventory = Inventory(owner=owner, element_name=name, element_uuid=element_uuid,
                                         related_ms=related_service)

        session.add(inventory)
        session.commit()
