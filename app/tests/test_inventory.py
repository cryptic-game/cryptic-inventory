from unittest import TestCase
from unittest.mock import patch

from mock.mock_loader import mock
from resources import inventory
from schemes import item_not_found, success


class TestInventory(TestCase):
    def setUp(self):
        mock.reset_mocks()

        self.query_inventory = mock.MagicMock()
        mock.wrapper.session.query.side_effect = {inventory.Inventory: self.query_inventory}.__getitem__

    def test_list_inventory(self):
        elements = [mock.MagicMock() for _ in range(5)]
        self.query_inventory.filter_by.return_value = elements
        self.assertEqual({"elements": [e.serialize for e in elements]}, inventory.list_inventory({}, "the-user"))
        self.query_inventory.filter_by.assert_called_with(owner="the-user")

    def test_exists_not_found(self):
        self.query_inventory.filter_by().first.return_value = None
        self.assertEqual({"exists": False}, inventory.exists({"owner": "the-user", "item_name": "my-item"}, ""))
        self.query_inventory.filter_by.assert_called_with(owner="the-user", element_name="my-item")
        self.query_inventory.filter_by().first.assert_called_with()

    def test_exists_found(self):
        self.query_inventory.filter_by().first.return_value = "item"
        self.assertEqual({"exists": True}, inventory.exists({"owner": "the-user", "item_name": "my-item"}, ""))
        self.query_inventory.filter_by.assert_called_with(owner="the-user", element_name="my-item")
        self.query_inventory.filter_by().first.assert_called_with()

    def test_create_not_found(self):
        self.assertEqual(
            item_not_found, inventory.create({"item_name": "does-not-exist", "owner": "", "related_ms": ""}, "")
        )

    @patch("resources.inventory.Inventory")
    def test_create_found(self, inventory_patch):
        self.assertEqual(
            inventory_patch.create().serialize,
            inventory.create({"item_name": "ATX", "owner": "user", "related_ms": "ms-name"}, ""),
        )
        inventory_patch.create.assert_called_with("ATX", "user", "ms-name")

    def test_remove_not_found(self):
        self.query_inventory.filter_by().first.return_value = None
        self.assertEqual(item_not_found, inventory.remove({"item_uuid": "item-uuid"}, ""))
        self.query_inventory.filter_by.assert_called_with(element_uuid="item-uuid")
        self.query_inventory.filter_by().first.assert_called_with()

    def test_remove_successful(self):
        self.query_inventory.filter_by().first.return_value = "item"
        self.assertEqual(success, inventory.remove({"item_uuid": "the-item"}, ""))
        self.query_inventory.filter_by.assert_called_with(element_uuid="the-item")
        self.query_inventory.filter_by().first.assert_called_with()
        mock.wrapper.session.delete.assert_called_with("item")
        mock.wrapper.session.commit.assert_called_with()

    def test_ms_list(self):
        elements = [mock.MagicMock() for _ in range(5)]
        self.query_inventory.filter_by.return_value = elements
        self.assertEqual({"elements": [e.serialize for e in elements]}, inventory.ms_list({"owner": "the-owner"}, ""))
        self.query_inventory.filter_by.assert_called_with(owner="the-owner")

    def test_delete_by_name_not_found(self):
        self.query_inventory.filter_by().first.return_value = None
        self.assertEqual(item_not_found, inventory.delete_by_name({"item_name": "item", "owner": "some-user"}, ""))
        self.query_inventory.filter_by.assert_called_with(element_name="item", owner="some-user")
        self.query_inventory.filter_by().first.assert_called_with()

    def test_delete_by_name_successful(self):
        self.query_inventory.filter_by().first.return_value = "item"
        self.assertEqual(success, inventory.delete_by_name({"item_name": "item", "owner": "some-user"}, ""))
        self.query_inventory.filter_by.assert_called_with(element_name="item", owner="some-user")
        self.query_inventory.filter_by().first.assert_called_with()
        mock.wrapper.session.delete.assert_called_with("item")
        mock.wrapper.session.commit.assert_called_with()
