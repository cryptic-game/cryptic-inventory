import app


# noinspection PyUnresolvedReferences
def load_endpoints():
    import resources.inventory
    import resources.shop


if __name__ == "__main__":
    load_endpoints()
    app.m.run()
