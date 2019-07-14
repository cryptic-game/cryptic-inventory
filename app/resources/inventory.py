from app import m, wrapper
from typing import List, Union
from models.Inventory import Inventory


@m.user_endpoint(path=["inventory", "list_inventory"], requires={})
def list_inventory(data: dict, user: str):
    query: List[Inventory] = wrapper.session.query(Inventory).filter_by(owner=user)

    inventory: List[List[Union[str, any]]] = [
        [element.element_name, element.element_uuid] for element in query
    ]

    return {"elements": inventory}


@m.microservice_endpoint(path=["inventory", "exist"])
def handle_ms(data: dict, microservice: str):
    query = wrapper.session.query(Inventory).filter_by(
        owner=data["owner"], element_name=data["name"]
    )

    if query is None:
        return {"exist": False}
    return {"exist": True}


@m.microservice_endpoint(path=["inventory", "remove"])
def remove(data: dict, microservice: str):
    query: Inventory = wrapper.session.query(Inventory).filter_by(
        element_uuid=data["uuid"]
    )

    wrapper.session.delete(query)
    wrapper.session.commit()

    return {"ok": True}


@m.microservice_endpoint(path=["inventory", "create"])
def create(data: dict, microservice: str):
    Inventory.create(data["name"], data["user"], data["service"])

    return {"ok": True}
