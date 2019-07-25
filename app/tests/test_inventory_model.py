from unittest import TestCase

from mock.mock_loader import mock
from models.inventory import Inventory


class TestInventoryModel(TestCase):
    def setUp(self):
        mock.reset_mocks()

    def test_structure(self):
        self.assertEqual("Inventory", Inventory.__tablename__)
        self.assertTrue(issubclass(Inventory, mock.wrapper.Base))
        for col in ["element_uuid", "element_name", "related_ms", "owner"]:
            self.assertTrue(col in dir(Inventory))

    def test_serialize(self):
        inventory = Inventory(element_uuid="element-uuid", element_name="name", related_ms="device", owner="the-owner")
        serialized = inventory.serialize
        self.assertEqual(
            {"element_uuid": "element-uuid", "element_name": "name", "related_ms": "device", "owner": "the-owner"},
            serialized,
        )
        serialized["element_uuid"] = "something-different"
        self.assertEqual(
            {"element_uuid": "element-uuid", "element_name": "name", "related_ms": "device", "owner": "the-owner"},
            inventory.serialize,
        )

    def test_create(self):
        result = Inventory.create("the-name", "some-user", "microservice-name")
        self.assertIsInstance(result, Inventory)
        self.assertEqual("the-name", result.element_name)
        self.assertEqual("some-user", result.owner)
        self.assertEqual("microservice-name", result.related_ms)
        self.assertRegex(result.element_uuid, r"[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}")
        mock.wrapper.session.add.assert_called_with(result)
        mock.wrapper.session.commit.assert_called_with()

    def test_create_different_uuid(self):
        self.assertNotEqual(
            Inventory.create("name", "owner", "ms").element_uuid, Inventory.create("name", "owner", "ms").element_uuid
        )
