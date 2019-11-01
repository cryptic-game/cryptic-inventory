from cryptic import MicroService, Config, DatabaseWrapper

m: MicroService = MicroService("inventory")

wrapper: DatabaseWrapper = m.get_wrapper()
