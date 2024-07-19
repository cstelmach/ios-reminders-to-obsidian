import json
import os
import re


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

    # Convert string patterns to regex objects
    if "listsToImport" in config:
        config["listsToImport"] = [
            (
                re.compile(pattern)
                if isinstance(pattern, str)
                and any(c in pattern for c in r".*?+^$()[]{|}\\")
                else pattern
            )
            for pattern in config["listsToImport"]
        ]

    return config


config = load_config()
