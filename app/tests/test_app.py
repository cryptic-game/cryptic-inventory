from importlib import machinery, util
from unittest import TestCase

from mock.mock_loader import mock
from schemes import shop_info, shop_buy, trade_requirements


def import_app(name: str = "app"):
    return machinery.SourceFileLoader(name, util.find_spec("app").origin).load_module()


class TestApp(TestCase):
    def setUp(self):
        mock.reset_mocks()

    def test__microservice_setup(self):
        app = import_app()

        mock.get_config.assert_called_with()
        self.assertEqual(mock.get_config(), app.config)

        mock.MicroService.assert_called_with("inventory")
        self.assertEqual(mock.MicroService(), app.m)

        mock.m.get_wrapper.assert_called_with()
        self.assertEqual(mock.m.get_wrapper(), app.wrapper)

    def test__run_as_main(self):
        import_app("__main__")

        mock.wrapper.Base.metadata.create_all.assert_called_with(bind=mock.wrapper.engine)
        mock.m.run.assert_called_with()

    def test__import_as_module(self):
        import_app()

        mock.wrapper.Base.metadata.create_all.assert_not_called()
        mock.m.run.assert_not_called()

    def test__endpoints_available(self):
        app = import_app("__main__")
        elements = [getattr(app, element_name) for element_name in dir(app)]

        registered_user_endpoints = mock.user_endpoints.copy()
        registered_ms_endpoints = mock.ms_endpoints.copy()

        expected_user_endpoints = [
            (["inventory", "trade"], trade_requirements),
            (["inventory", "list"], {}),
            (["shop", "list"], {}),
            (["shop", "info"], shop_info),
            (["shop", "buy"], shop_buy),
        ]

        expected_ms_endpoints = [
            ["inventory", "exists"],
            ["inventory", "create"],
            ["inventory", "remove"],
            ["inventory", "list"],
            ["inventory", "delete_by_name"],
        ]

        for path, requires in expected_user_endpoints:
            self.assertIn((path, requires), registered_user_endpoints)
            registered_user_endpoints.remove((path, requires))
            self.assertIn(mock.user_endpoint_handlers[tuple(path)], elements)

        for path in expected_ms_endpoints:
            self.assertIn(path, registered_ms_endpoints)
            registered_ms_endpoints.remove(path)
            self.assertIn(mock.ms_endpoint_handlers[tuple(path)], elements)

        self.assertFalse(registered_user_endpoints)
        self.assertFalse(registered_ms_endpoints)
