import configparser

def write_default():
    default_data = {
        "server": {
            "host": "ws://localhost:5555/ws"
        },
        "client": {
            "icon_path": "assets/icon.ico"
        }
    }

    config = configparser.ConfigParser()

    for section in default_data:
        config[section] = default_data[section]

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def update_config(**kwargs):
    config = configparser.ConfigParser()
    config.read("config.ini")

    for section in kwargs:
        for key in kwargs[section]:
            if section not in config:
                config[section] = {}
                
            config[section][key] = kwargs[section][key]
    
    with open('config.ini', 'w') as configfile:
        config.write(configfile)