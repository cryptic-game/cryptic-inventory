from unittest import TestCase
from unittest.mock import patch

from mock.mock_loader import mock
from resources import shop
from vars import game_info


class TestShop(TestCase):
    def setUp(self):
        mock.reset_mocks()

    def test__exists_wallet__not_found(self):
        mock.MicroService().contact_microservice.return_value = {"exists": False}

        actual_result = shop.exists_wallet("test-wallet")

        self.assertFalse(actual_result)
        mock.MicroService().contact_microservice.assert_called_with(
            "currency", ["exists"], {"source_uuid": "test-wallet"}
        )

    def test__exists_wallet__successful(self):
        mock.MicroService().contact_microservice.return_value = {"exists": True}

        actual_result = shop.exists_wallet("test-wallet")

        self.assertTrue(actual_result)
        mock.MicroService().contact_microservice.assert_called_with(
            "currency", ["exists"], {"source_uuid": "test-wallet"}
        )

    def test__pay_shop(self):
        expected_result = "whatever_currency_returns"

        mock.MicroService().contact_microservice.return_value = expected_result

        actual_result = shop.pay_shop("my-wallet", "wallet-key", 1337, {"foo": 42, "bar": 1337})

        self.assertEqual(expected_result, actual_result)
        mock.MicroService().contact_microservice.assert_called_with(
            "currency",
            ["dump"],
            {
                "source_uuid": "my-wallet",
                "key": "wallet-key",
                "amount": 1337,
                "create_transaction": True,
                "destination_uuid": "00000000-0000-0000-0000-000000000000",
                "origin": 1,
                "usage": "Payment for 42x foo, 1337x bar",
            },
        )

    def test__user_endpoint__shop_list(self):
        items = game_info["items"]
        expected_result = {
            "products": [
                {
                    "name": name,
                    "price": items[name]["price"],
                    "related_ms": items[name]["related_ms"],
                    "category": items[name]["category"],
                }
                for name in items
            ]
        }
        actual_result = shop.shop_list({}, "")

        self.assertEqual(expected_result, actual_result)

    def test__user_endpoint__shop_info__item_not_found(self):
        expected_result = {"error": "item_not_found"}
        actual_result = shop.shop_info({"product": "does_not_exist"}, "")

        self.assertEqual(expected_result, actual_result)

    def test__user_endpoint__shop_info__successful(self):
        expected_result = {
            "name": "ATX",
            "price": game_info["items"]["ATX"]["price"],
            "related_ms": "device",
            "category": "case",
        }
        actual_result = shop.shop_info({"product": "ATX"}, "")

        self.assertEqual(expected_result, actual_result)

    def test__user_endpoint__shop_buy__item_not_found(self):
        expected_result = {"error": "item_not_found"}
        actual_result = shop.shop_buy({"products": {"does-not-exist": 1}, "wallet_uuid": "", "key": ""}, "")

        self.assertEqual(expected_result, actual_result)

    @patch("resources.shop.exists_wallet")
    def test__user_endpoint__shop_buy__wallet_not_found(self, exists_wallet_patch):
        exists_wallet_patch.return_value = False

        expected_result = {"error": "wallet_not_found"}
        actual_result = shop.shop_buy({"products": {"ATX": 1}, "wallet_uuid": "test-wallet", "key": "the-key"}, "")

        self.assertEqual(expected_result, actual_result)
        exists_wallet_patch.assert_called_with("test-wallet")

    @patch("resources.shop.pay_shop")
    @patch("resources.shop.exists_wallet")
    def test__user_endpoint__shop_buy__invalid_wallet(self, exists_wallet_patch, pay_shop_patch):
        expected_result = {"error": "some-error", "foo": "bar"}

        exists_wallet_patch.return_value = True
        pay_shop_patch.return_value = expected_result

        actual_result = shop.shop_buy({"products": {"ATX": 1}, "wallet_uuid": "test-wallet", "key": "wallet-key"}, "")

        self.assertEqual(expected_result, actual_result)
        pay_shop_patch.assert_called_with("test-wallet", "wallet-key", game_info["items"]["ATX"]["price"], {"ATX": 1})

    @patch("resources.shop.Inventory")
    @patch("resources.shop.pay_shop")
    @patch("resources.shop.exists_wallet")
    def test__user_endpoint__shop_buy__successful(self, exists_wallet_patch, pay_shop_patch, inventory_patch):
        exists_wallet_patch.return_value = True
        pay_shop_patch.return_value = {"success": True}

        expected_result = {"bought_products": [inventory_patch.create().serialize]}
        actual_result = shop.shop_buy({"products": {"ATX": 1}, "wallet_uuid": "wallet", "key": "key"}, "the-user")

        self.assertEqual(expected_result, actual_result)
        inventory_patch.create.assert_called_with("ATX", "the-user", "device")
