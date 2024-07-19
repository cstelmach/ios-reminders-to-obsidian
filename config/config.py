import json
import os


def load_config(config_file="data.json", default_config_file="data_default.json"):
    config_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(config_dir, config_file)
    default_config_path = os.path.join(config_dir, default_config_file)

    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            config = json.load(file)
    else:
        with open(default_config_path, "r") as file:
            config = json.load(file)
    return config


config = load_config()
