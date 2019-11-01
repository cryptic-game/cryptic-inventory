from cryptic import MicroService, DatabaseWrapper

m: MicroService = MicroService("inventory")

wrapper: DatabaseWrapper = m.get_wrapper()
wrapper.Base.metadata.create_all(bind=wrapper.engine)
