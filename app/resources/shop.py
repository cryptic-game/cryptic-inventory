from app import m
from models.inventory import Inventory
from schemes import *
from vars import game_info


def exists_wallet(wallet: str) -> bool:
    return m.contact_microservice("currency", ["exists"], {"source_uuid": wallet})[
        "exists"
    ]


def pay_shop(wallet: str, key: str, amount: int, product: str) -> dict:
    return m.contact_microservice(
        "currency",
        ["dump"],
        {
            "source_uuid": wallet,
            "key": key,
            "amount": amount,
            "create_transaction": True,
            "destination_uuid": "00000000-0000-0000-0000-000000000000",
            "usage": f"Payment for {product}",
            "origin": 1,
        },
    )


@m.user_endpoint(path=["shop", "list"], requires={})
def shop_list(data: dict, user: str):
    return {"products": list(game_info["items"])}


@m.user_endpoint(path=["shop", "info"], requires=shop_info)
def shop_info(data: dict, user: str):
    product: str = data["product"]

    if product not in game_info["items"]:
        return item_not_found

    return {"name": product, **game_info["items"][product]}


@m.user_endpoint(path=["shop", "buy"], requires=shop_buy)
def shop_buy(data: dict, user: str):
    product: str = data["product"]
    wallet_uuid: str = data["wallet_uuid"]
    key: str = data["key"]

    if product not in game_info["items"]:
        return item_not_found

    if not exists_wallet(wallet_uuid):
        return wallet_not_found

    price: int = game_info["items"][product]["price"]

    response: dict = pay_shop(wallet_uuid, key, price, product)
    if "error" in response:
        return response

    item: Inventory = Inventory.create(
        product, user, game_info["items"][product]["related_ms"]
    )

    return item.serialize
