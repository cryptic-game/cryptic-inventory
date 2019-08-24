from scheme import Text, UUID

shop_info: dict = {"product": Text(nonempty=True)}

shop_buy: dict = {"product": Text(nonempty=True), "wallet_uuid": UUID(), "key": Text(pattern=r"^[a-f0-9]{10}$")}

trade_requirements: dict = {"element_uuid": UUID(), "target": UUID()}

success: dict = {"ok": True}

item_not_found: dict = {"error": "item_not_found"}

wallet_not_found: dict = {"error": "wallet_not_found"}

user_uuid_does_not_exist: dict = {"error": "user_uuid_does_not_exist"}

cannot_trade_with_yourself: dict = {"error": "cannot_trade_with_yourself"}
