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

    if not config["server"].get("host"):
        update_config(server={"host": default_data["server"]["host"]})
    if not config["server"].get("version"):
        update_config(server={"version": default_data["server"]["version"]})
    if not config["client"].get("icon_path"):
        update_config(client={"icon_path": default_data["client"]["icon_path"]})
    if not config["client"].get("theme"):
        update_config(client={"theme": default_data["client"]["theme"]})

    if config["server"]["version"] != default_data["server"]["version"]:
        update_config(server={"version": default_data["server"]["version"]})