from app import m
from typing import List, Union
from models.Inventory import Inventory
from objects import *
from scheme import *


@m.user_endpoint(path=["list_inventory"], requires={"user": Text(required=True, nonempy=True)})
def list_inventory(data: dict, user: str):
    query: List[Inventory] = session.query(Inventory).filter_by(owner=user)

    inventory: List[List[Union[str, any]]] = [[element.element_name, element.element_uuid] for element in query]

    return {"elements": inventory}


@m.microservice_endpoint(path=["exist"])
def handle_ms(data: dict, microservice: str):
    query = session.query(Inventory).filter_by(owner=data["owner"], element_name=data["name"])

    if query is None:
        return {"exist": False}
    return {"exist": True}


@m.microservice_endpoint(path=["remove"])
def remove(data: dict, microservice: str):
    query: Inventory = session.query(Inventory).filter_by(element_uuid=data["uuid"])

    session.delete(query)
    session.commit()

    return {"ok": True}


@m.microservice_endpoint(path=["create"])
def create(data: dict, microservice: str):
    Inventory.create(data["name"], data["user"], data["service"])

    return {"ok": True}
