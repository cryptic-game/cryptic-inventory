from app import m
from typing import List
from vars import config as game_info
from schemes import (
    this_item_does_not_exists,
    shop_info,
    shop_buy,
    wallet_does_not_exists,
)
from models.Inventory import Inventory


def check_wallet(wallet: str) -> bool:
    return m.contact_microservice("currency", ["exists"], {"source_uuid": wallet})[
        "exists"
    ]


def pay_shop(wallet: str, key: str, amount: int) -> dict:
    return m.contact_microservice(
        "currency", ["dump"], {"source_uuid": wallet, "key": key, "amount": amount}
    )


@m.user_endpoint(path=["shop", "list"], requires={})
def _shop_list(data: dict, user: str):

    products: List[str] = game_info["items"].key()

    return {"products": products}


@m.user_endpoint(path=["shop", "info"], requires=shop_info)
def _shop_info(data: dict, user: str):

    if not data["product"] in game_info["items"].key():
        return this_item_does_not_exists

    return {"name": data["product"], "info": game_info["items"][data["product"]]}


@m.user_endpoint(path=["shop", "buy"], requires=shop_buy)
def _shop_buy(data: dict, user: str):

    if not data["product"] in game_info["items"].key():
        return this_item_does_not_exists

    if not check_wallet(data["wallet_uuid"]):
        return wallet_does_not_exists

    price: int = game_info["items"]["product"]["price"]

    response: dict = pay_shop(data["wallet"], data["key"], price)

    if "error" in response:
        return response

    else:

        inv: Inventory = Inventory.create(
            data["name"], user, game_info["items"]["product"]["related_ms"]
        )

        return inv.serialize
