import configparser

default_data = {
    "server": {
        "host": "ws://sch.nawafdev.com/ws",
        "version": "1.0.0-beta3"
    },
    "client": {
        "icon_path": "icon.ico",
        "notifications": "False",
        "theme": "SCH"
    }
}

def write_default():

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