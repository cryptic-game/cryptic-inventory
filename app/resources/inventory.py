from typing import Optional, Dict

from app import m, wrapper
from models.inventory import Inventory
from schemes import *
from vars import game_info


@m.user_endpoint(path=["inventory", "trade"], requires=trade_requirements)
def trade(data: dict, user: str) -> dict:
    element: Optional[Inventory] = wrapper.session.query(Inventory).get(data["element_uuid"])
    target: str = data["target"]

    if element is None or element.owner != user:
        return item_not_found
    if element.owner == target:
        return cannot_trade_with_yourself
    if not m.check_user_uuid(target):
        return user_uuid_does_not_exist

    element.owner = target
    wrapper.session.commit()

    return success


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


@m.microservice_endpoint(path=["inventory", "summary"])
def summary(data: dict, microservice: str) -> dict:
    out: Dict[str, int] = {}
    for element in wrapper.session.query(Inventory).filter_by(owner=data["owner"]):  # type: Inventory
        out[element.element_name] = out.get(element.element_name, 0) + 1
    return {"elements": out}


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


@m.microservice_endpoint(path=["delete_user"])
def delete_user(data: dict, microservice: str) -> dict:
    user: str = data["user_uuid"]

    wrapper.session.query(Inventory).filter_by(owner=user).delete()
    wrapper.session.commit()

    return success
