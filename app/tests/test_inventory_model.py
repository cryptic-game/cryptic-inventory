from unittest import TestCase

from mock.mock_loader import mock
from models.inventory import Inventory


class TestInventoryModel(TestCase):
    def setUp(self):
        mock.reset_mocks()

    def test__model__inventory__structure(self):
        self.assertEqual("Inventory", Inventory.__tablename__)
        self.assertTrue(issubclass(Inventory, mock.wrapper.Base))
        for col in ["element_uuid", "element_name", "related_ms", "owner"]:
            self.assertTrue(col in dir(Inventory))

    def test__model__inventory__serialize(self):
        inventory = Inventory(element_uuid="element-uuid", element_name="name", related_ms="device", owner="the-owner")

        expected_result = {
            "element_uuid": "element-uuid",
            "element_name": "name",
            "related_ms": "device",
            "owner": "the-owner",
        }
        serialized = inventory.serialize

        self.assertEqual(expected_result, serialized)

        serialized["element_uuid"] = "something-different"
        self.assertEqual(expected_result, inventory.serialize)

    def test__model__inventory__create(self):
        actual_result = Inventory.create("the-name", "some-user", "microservice-name")

        self.assertIsInstance(actual_result, Inventory)
        self.assertEqual("the-name", actual_result.element_name)
        self.assertEqual("some-user", actual_result.owner)
        self.assertEqual("microservice-name", actual_result.related_ms)
        self.assertRegex(actual_result.element_uuid, r"[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}")
        mock.wrapper.session.add.assert_called_with(actual_result)
        mock.wrapper.session.commit.assert_called_with()

    def test__model__inventory__create__different_uuid(self):
        first_element = Inventory.create("name", "owner", "ms").element_uuid
        second_element = Inventory.create("name", "owner", "ms").element_uuid
        self.assertNotEqual(first_element, second_element)
