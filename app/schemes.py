from scheme import Text, UUID

shop_info: dict = {"product": Text(nonempty=True)}

shop_buy: dict = {"product": Text(nonempty=True), "wallet_uuid": UUID(), "key": Text(pattern=r"^[a-f0-9]{10}$")}

success: dict = {"ok": True}

item_not_found: dict = {"error": "item_not_found"}

wallet_not_found: dict = {"error": "wallet_not_found"}
