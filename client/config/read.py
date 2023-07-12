import configparser
from .write import write_default, update_config, default_data

def read_config():
    check_config()

    config = configparser.ConfigParser()
    config.read("config.ini")

    return config

def check_config():
    config = configparser.ConfigParser()
    config.read("config.ini")

    if "server" not in config or "client" not in config:
        write_default()
        return

    for key in default_data["server"]:
        if key not in config["server"]:
            update_config(server={key: default_data["server"][key]})
    for key in default_data["client"]:
        if key not in config["client"]:
            update_config(client={key: default_data["client"][key]})
            
    if config["server"]["version"] != default_data["server"]["version"]:
        update_config(server={"version": default_data["server"]["version"]})