from scheme import Text, UUID
from typing import Dict

shop_info: dict = {"product": Text(required=True, nonempty=True)}

shop_buy: dict = {
    "wallet_uuid": UUID(),
    "name": Text(required=True, nonempty=True),
    "key": Text(required=True, nonempty=True),
}

this_item_does_not_exists: Dict[str, str] = {"error": "this_item_does_not_exists"}

wallet_does_not_exists: Dict[str, str] = {"error": "this_wallet_does_not_exists"}

success: Dict[str, bool] = {"ok": True}
