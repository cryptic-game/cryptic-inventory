from unittest import TestCase
from unittest.mock import patch

from mock.mock_loader import mock
from resources import shop
from schemes import item_not_found, wallet_not_found
from vars import game_info


class TestShop(TestCase):
    def setUp(self):
        mock.reset_mocks()

    def test__exists_wallet__not_found(self):
        mock.MicroService().contact_microservice.return_value = {"exists": False}
        self.assertFalse(shop.exists_wallet("test-wallet"))
        mock.MicroService().contact_microservice.assert_called_with(
            "currency", ["exists"], {"source_uuid": "test-wallet"}
        )

    def test__exists_wallet__successful(self):
        mock.MicroService().contact_microservice.return_value = {"exists": True}
        self.assertTrue(shop.exists_wallet("test-wallet"))
        mock.MicroService().contact_microservice.assert_called_with(
            "currency", ["exists"], {"source_uuid": "test-wallet"}
        )

    def test__pay_shop(self):
        mock.MicroService().contact_microservice.return_value = "whatever_currency_returns"
        self.assertEqual("whatever_currency_returns", shop.pay_shop("my-wallet", "wallet-key", 1337, "test-product"))
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
                "usage": "Payment for test-product",
            },
        )

    def test__user_endpoint__shop_list(self):
        self.assertEqual({"products": list(game_info["items"])}, shop.shop_list({}, ""))

    def test__user_endpoint__shop_info__item_not_found(self):
        self.assertEqual(item_not_found, shop.shop_info({"product": "does_not_exist"}, ""))

    def test__user_endpoint__shop_info__successful(self):
        self.assertEqual({"name": "ATX", "price": 100, "related_ms": "device"}, shop.shop_info({"product": "ATX"}, ""))

    def test__user_endpoint__shop_buy__item_not_found(self):
        self.assertEqual(item_not_found, shop.shop_buy({"product": "does-not-exist", "wallet_uuid": "", "key": ""}, ""))

    @patch("resources.shop.exists_wallet")
    def test__user_endpoint__shop_buy__wallet_not_found(self, exists_wallet_patch):
        exists_wallet_patch.return_value = False
        self.assertEqual(
            wallet_not_found, shop.shop_buy({"product": "ATX", "wallet_uuid": "test-wallet", "key": "the-key"}, "")
        )
        exists_wallet_patch.assert_called_with("test-wallet")

    @patch("resources.shop.pay_shop")
    @patch("resources.shop.exists_wallet")
    def test__user_endpoint__shop_buy__invalid_wallet(self, exists_wallet_patch, pay_shop_patch):
        exists_wallet_patch.return_value = True
        pay_shop_patch.return_value = {"error": "some-error", "foo": "bar"}
        self.assertEqual(
            {"error": "some-error", "foo": "bar"},
            shop.shop_buy({"product": "ATX", "wallet_uuid": "test-wallet", "key": "wallet-key"}, ""),
        )
        pay_shop_patch.assert_called_with("test-wallet", "wallet-key", 100, "ATX")

    @patch("resources.shop.Inventory")
    @patch("resources.shop.pay_shop")
    @patch("resources.shop.exists_wallet")
    def test__user_endpoint__shop_buy__successful(self, exists_wallet_patch, pay_shop_patch, inventory_patch):
        exists_wallet_patch.return_value = True
        pay_shop_patch.return_value = {"success": True}
        self.assertEqual(
            inventory_patch.create().serialize,
            shop.shop_buy({"product": "ATX", "wallet_uuid": "wallet", "key": "key"}, "the-user"),
        )
        inventory_patch.create.assert_called_with("ATX", "the-user", "device")
