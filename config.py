import json
import os

def load_config(config_file='data.json', default_config_file='data_default.json'):
    if os.path.exists(config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
    else:
        with open(default_config_file, 'r') as file:
            config = json.load(file)
    return config

config = load_config()