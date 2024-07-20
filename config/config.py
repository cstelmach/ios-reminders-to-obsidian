# ios_reminders_to_markdown_journal/config/config.py

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

    # Flatten the config for easier access
    flat_config = {}
    for section, values in config.items():
        for key, value in values.items():
            flat_config[key] = value

    # Convert string patterns to regex objects for listsToImport and listsToOmit
    for key in ["listsToImport", "listsToOmit"]:
        if key in flat_config:
            flat_config[key] = [
                (
                    re.compile(pattern)
                    if isinstance(pattern, str)
                    and any(c in pattern for c in r".*?+^$()[]{|}\\")
                    else pattern
                )
                for pattern in flat_config[key]
            ]

    # Handle the sections dictionary
    if "sectionsToHide" in flat_config:
        flat_config["sectionsToHide"] = [
            (
                re.compile(pattern)
                if isinstance(pattern, str)
                and any(c in pattern for c in r".*?+^$()[]{|}\\")
                else pattern
            )
            for pattern in flat_config["sectionsToHide"]
        ]

    if "sectionsToAddAsTags" in flat_config:
        flat_config["sectionsToAddAsTags"] = [
            (re.compile(pattern), tag)
            for pattern, tag in flat_config["sectionsToAddAsTags"]
        ]

    return flat_config


config = load_config()
