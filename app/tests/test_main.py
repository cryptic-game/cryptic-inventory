from importlib import machinery, util
from unittest import TestCase

from mock.mock_loader import mock
from resources import inventory, shop
from schemes import shop_info, shop_buy, trade_requirements


def import_app(name: str = "app"):
    return machinery.SourceFileLoader(name, util.find_spec("app").origin).load_module()


def import_main(name: str = "main"):
    return machinery.SourceFileLoader(name, util.find_spec("main").origin).load_module()


class TestApp(TestCase):
    def setUp(self):
        mock.reset_mocks()

    def test__microservice_setup(self):
        app = import_app()

        mock.MicroService.assert_called_with("inventory")
        self.assertEqual(mock.MicroService(), app.m)

        mock.m.get_wrapper.assert_called_with()
        self.assertEqual(mock.m.get_wrapper(), app.wrapper)

    def test__microservice_setup_called(self):
        main = import_main()
        self.assertEqual(import_app(), main.app)

    def test__run_as_main(self):
        import_main("__main__")

        mock.wrapper.Base.metadata.create_all.assert_called_with(bind=mock.wrapper.engine)
        mock.m.run.assert_called_with()

    def test__import_as_module(self):
        import_main()

        mock.wrapper.Base.metadata.create_all.assert_not_called()
        mock.m.run.assert_not_called()

    def test__endpoints_available(self):
        main = import_main("__main__")
        elements = [getattr(main, element_name) for element_name in dir(main)]

        registered_user_endpoints = mock.user_endpoints.copy()
        registered_ms_endpoints = mock.ms_endpoints.copy()

        expected_user_endpoints = [
            (["inventory", "trade"], trade_requirements, inventory.trade),
            (["inventory", "list"], {}, inventory.list_inventory),
            (["shop", "list"], {}, shop.shop_list),
            (["shop", "info"], shop_info, shop.shop_info),
            (["shop", "buy"], shop_buy, shop.shop_buy),
        ]

        expected_ms_endpoints = [
            (["inventory", "exists"], inventory.exists),
            (["inventory", "create"], inventory.create),
            (["inventory", "remove"], inventory.remove),
            (["inventory", "list"], inventory.ms_list),
            (["inventory", "summary"], inventory.summary),
            (["inventory", "delete_by_name"], inventory.delete_by_name),
            (["delete_user"], inventory.delete_user),
        ]

        for path, requires, func in expected_user_endpoints:
            self.assertIn((path, requires), registered_user_endpoints)
            registered_user_endpoints.remove((path, requires))
            self.assertIn(mock.user_endpoint_handlers[tuple(path)], elements)
            self.assertEqual(func, mock.user_endpoint_handlers[tuple(path)])

        for path, func in expected_ms_endpoints:
            self.assertIn(path, registered_ms_endpoints)
            registered_ms_endpoints.remove(path)
            self.assertIn(mock.ms_endpoint_handlers[tuple(path)], elements)
            self.assertEqual(func, mock.ms_endpoint_handlers[tuple(path)])

        self.assertFalse(registered_user_endpoints)
        self.assertFalse(registered_ms_endpoints)
