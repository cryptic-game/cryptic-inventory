from importlib import machinery, util
from unittest import TestCase

from mock.mock_loader import mock
from schemes import shop_info, shop_buy


def import_app(name: str = "app"):
    return machinery.SourceFileLoader(name, util.find_spec("app").origin).load_module()


class TestApp(TestCase):
    def setUp(self):
        mock.reset_mocks()

    def test_setup(self):
        app = import_app()
        mock.get_config.assert_called_with()
        self.assertEqual(mock.get_config(), app.config)
        mock.MicroService.assert_called_with("inventory")
        self.assertEqual(mock.MicroService(), app.m)
        mock.m.get_wrapper.assert_called_with()
        self.assertEqual(mock.m.get_wrapper(), app.wrapper)

    def test_main(self):
        import_app("__main__")
        mock.wrapper.Base.metadata.create_all.assert_called_with(bind=mock.wrapper.engine)
        mock.m.run.assert_called_with()

    def test_not_main(self):
        import_app()
        mock.wrapper.Base.metadata.create_all.assert_not_called()
        mock.m.run.assert_not_called()

    def test_endpoints(self):
        app = import_app("__main__")
        elements = [getattr(app, element_name) for element_name in dir(app)]

        for path, requires in [
            (["inventory", "list"], {}),
            (["shop", "list"], {}),
            (["shop", "info"], shop_info),
            (["shop", "buy"], shop_buy),
        ]:
            self.assertIn((path, requires), mock.user_endpoints)
            self.assertIn(mock.user_endpoint_handlers[tuple(path)], elements)

        for path in [
            ["inventory", "exists"],
            ["inventory", "create"],
            ["inventory", "remove"],
            ["inventory", "list"],
            ["inventory", "delete_by_name"],
        ]:
            self.assertIn(path, mock.ms_endpoints)
            self.assertIn(mock.ms_endpoint_handlers[tuple(path)], elements)