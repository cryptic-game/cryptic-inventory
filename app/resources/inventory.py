from typing import Optional

from app import m, wrapper
from models.inventory import Inventory
from schemes import *
from vars import game_info


@m.user_endpoint(path=["inventory", "list"], requires={})
def list_inventory(data: dict, user: str) -> dict:
    return {"elements": [element.serialize for element in wrapper.session.query(Inventory).filter_by(owner=user)]}


@m.microservice_endpoint(path=["inventory", "exists"])
def exists(data: dict, microservice: str) -> dict:
    item: Optional[Inventory] = wrapper.session.query(Inventory).filter_by(
        owner=data["owner"], element_name=data["item_name"]
    ).first()

    return {"exists": item is not None}


@m.microservice_endpoint(path=["inventory", "create"])
def create(data: dict, microservice: str) -> dict:
    name: str = data["item_name"]
    if name not in game_info["items"]:
        return item_not_found

    item: Inventory = Inventory.create(name, data["owner"], data["related_ms"])

    return item.serialize


@m.microservice_endpoint(path=["inventory", "remove"])
def remove(data: dict, microservice: str) -> dict:
    item: Inventory = wrapper.session.query(Inventory).filter_by(element_uuid=data["item_uuid"]).first()

    if item is None:
        return item_not_found

    wrapper.session.delete(item)
    wrapper.session.commit()

    return success


@m.microservice_endpoint(path=["inventory", "list"])
def ms_list(data: dict, microservice: str) -> dict:
    return {
        "elements": [element.serialize for element in wrapper.session.query(Inventory).filter_by(owner=data["owner"])]
    }


@m.microservice_endpoint(path=["inventory", "delete_by_name"])
def delete_by_name(data: dict, microservice: str) -> dict:
    item: Inventory = wrapper.session.query(Inventory).filter_by(
        element_name=data["item_name"], owner=data["owner"]
    ).first()

    if item is None:
        return item_not_found

    wrapper.session.delete(item)
    wrapper.session.commit()

    return success
