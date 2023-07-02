import configparser
from .write import write_default

def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')

    if len(config.sections()) == 0:
        write_default()

        return read_config()

    return config