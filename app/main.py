import app

if __name__ == "__main__":
    from resources.inventory import *
    from resources.shop import *

    app.wrapper.Base.metadata.create_all(bind=wrapper.engine)

    app.m.run()
