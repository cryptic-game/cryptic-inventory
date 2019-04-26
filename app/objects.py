from cryptic import MicroService, setup_database, get_config, Config
import argparse

parser: argparse.ArgumentParser = argparse.ArgumentParser()

parser.add_argument('--debug', help='run this service with sqlite instead of mysql only for use in develop environment',
                    default=False, action='store_true')

args: argparse.Namespace = parser.parse_args()

if args.debug is True:

    config: Config = get_config(mode="debug")

else:

    config: Config = get_config(mode="prod")

engine, Base, session = setup_database()
