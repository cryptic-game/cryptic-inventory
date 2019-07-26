from unittest import TestCase
from unittest.mock import patch

from mock.mock_loader import mock
from resources import inventory


class TestInventory(TestCase):
    def setUp(self):
        mock.reset_mocks()

        self.query_inventory = mock.MagicMock()
        mock.wrapper.session.query.side_effect = {inventory.Inventory: self.query_inventory}.__getitem__

    def test__user_endpoint__inventory_list(self):
        elements = [mock.MagicMock() for _ in range(5)]

        self.query_inventory.filter_by.return_value = elements

        expected_result = {"elements": [e.serialize for e in elements]}
        actual_result = inventory.list_inventory({}, "the-user")

        self.assertEqual(expected_result, actual_result)
        self.query_inventory.filter_by.assert_called_with(owner="the-user")

    def test__ms_endpoint__inventory_exists__item_not_found(self):
        self.query_inventory.filter_by().first.return_value = None

        expected_result = {"exists": False}
        actual_result = inventory.exists({"owner": "the-user", "item_name": "my-item"}, "")

        self.assertEqual(expected_result, actual_result)
        self.query_inventory.filter_by.assert_called_with(owner="the-user", element_name="my-item")
        self.query_inventory.filter_by().first.assert_called_with()

    def test__ms_endpoint__inventory_exists__item_found(self):
        self.query_inventory.filter_by().first.return_value = "item"

        expected_result = {"exists": True}
        actual_result = inventory.exists({"owner": "the-user", "item_name": "my-item"}, "")

        self.assertEqual(expected_result, actual_result)
        self.query_inventory.filter_by.assert_called_with(owner="the-user", element_name="my-item")
        self.query_inventory.filter_by().first.assert_called_with()

    def test__ms_endpoint__inventory_create__item_not_found(self):
        expected_result = {"error": "item_not_found"}
        actual_result = inventory.create({"item_name": "does-not-exist", "owner": "", "related_ms": ""}, "")

        self.assertEqual(expected_result, actual_result)

    @patch("resources.inventory.Inventory")
    def test__ms_endpoint__inventory_create__successful(self, inventory_patch):
        expected_result = inventory_patch.create().serialize
        actual_result = inventory.create({"item_name": "ATX", "owner": "user", "related_ms": "ms-name"}, "")

        self.assertEqual(expected_result, actual_result)
        inventory_patch.create.assert_called_with("ATX", "user", "ms-name")

    def test__ms_endpoint__inventory_remove__item_not_found(self):
        self.query_inventory.filter_by().first.return_value = None

        expected_result = {"error": "item_not_found"}
        actual_result = inventory.remove({"item_uuid": "item-uuid"}, "")

        self.assertEqual(expected_result, actual_result)
        self.query_inventory.filter_by.assert_called_with(element_uuid="item-uuid")
        self.query_inventory.filter_by().first.assert_called_with()

    def test__ms_endpoint__inventory_remove__successful(self):
        self.query_inventory.filter_by().first.return_value = "item"

        expected_result = {"ok": True}
        actual_result = inventory.remove({"item_uuid": "the-item"}, "")

        self.assertEqual(expected_result, actual_result)
        self.query_inventory.filter_by.assert_called_with(element_uuid="the-item")
        self.query_inventory.filter_by().first.assert_called_with()
        mock.wrapper.session.delete.assert_called_with("item")
        mock.wrapper.session.commit.assert_called_with()

    def test__ms_endpoint__inventory_list(self):
        elements = [mock.MagicMock() for _ in range(5)]

        self.query_inventory.filter_by.return_value = elements

        expected_result = {"elements": [e.serialize for e in elements]}
        actual_result = inventory.ms_list({"owner": "the-owner"}, "")

        self.assertEqual(expected_result, actual_result)
        self.query_inventory.filter_by.assert_called_with(owner="the-owner")

    def test__ms_endpoint__inventory_delete_by_name__item_not_found(self):
        self.query_inventory.filter_by().first.return_value = None

        expected_result = {"error": "item_not_found"}
        actual_result = inventory.delete_by_name({"item_name": "item", "owner": "some-user"}, "")

        self.assertEqual(expected_result, actual_result)
        self.query_inventory.filter_by.assert_called_with(element_name="item", owner="some-user")
        self.query_inventory.filter_by().first.assert_called_with()

    def test__ms_endpoint__inventory_delete_by_name__successful(self):
        self.query_inventory.filter_by().first.return_value = "item"

        expected_result = {"ok": True}
        actual_result = inventory.delete_by_name({"item_name": "item", "owner": "some-user"}, "")

        self.assertEqual(expected_result, actual_result)
        self.query_inventory.filter_by.assert_called_with(element_name="item", owner="some-user")
        self.query_inventory.filter_by().first.assert_called_with()
        mock.wrapper.session.delete.assert_called_with("item")
        mock.wrapper.session.commit.assert_called_with()
