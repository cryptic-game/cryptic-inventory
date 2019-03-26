from resources.property import handle, handle_ms
from cryptic import MicroService


if __name__ == '__main__':
    m = MicroService('service', handle, handle_ms)
    m.run()
