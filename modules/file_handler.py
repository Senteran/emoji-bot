import configparser

config = configparser.ConfigParser()

def get_value(key):
    config.read('data/values.ini')
    try:
        return config['DEFAULT'][key]
    except:
        print(f'Failed to get key {key}')

def store_value(key, value):
    config.read('data/values.ini')
    config['DEFAULT'][key] = value
    with open('data/values.ini', 'w') as configfile:
        config.write(configfile)