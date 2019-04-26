from cryptic import MicroService

m = MicroService(name='inventory')

if __name__ == '__main__':
    import resources.inventory

    m.run()
