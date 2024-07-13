import os
import json
from config import config
from header_utils import write_section_header
from append_reminders import append_reminders


def get_paths_and_template():
    folder_path = (
        config["dailyNoteFolderOverwrite"]
        if config["dailyNoteFolderOverwrite"]
        else None
    )
    date_format = (
        config["dailyNoteFilenameOverwrite"]
        if config["dailyNoteFilenameOverwrite"]
        else None
    )
    template_path = config["templateOverwritePath"]

    if not folder_path or not date_format:
        obsidian_parent_path = os.path.dirname(config["obsidianSettingsPath"])
        periodic_notes_config_path = os.path.join(
            obsidian_parent_path, "plugins/periodic-notes/data.json"
        )
        with open(periodic_notes_config_path, "r") as file:
            periodic_notes_config = json.load(file)
            daily_config = periodic_notes_config.get("daily", {})
            if not folder_path:
                folder_path = os.path.join(
                    obsidian_parent_path, daily_config.get("folder")
                )
            if not date_format:
                date_format = daily_config.get("format")
            if not template_path:
                template_path = os.path.join(
                    obsidian_parent_path, daily_config.get("template")
                )

    return folder_path, date_format, template_path


def create_file_if_not_exists(filename, template_path):
    if not os.path.exists(filename):
        with open(filename, "w") as file:
            if template_path and os.path.exists(template_path):
                with open(template_path, "r") as template_file:
                    file.write(template_file.read())
            else:
                file.write("\n\n")


def append_reminders_to_file(filename, reminders, section_header_exists, reminder_list):
    with open(filename, "a") as file:
        if not section_header_exists:
            write_section_header(
                file, config["sectionHeader"], config["sectionHeaderLevel"]
            )
        else:
            file.write("\n")
        append_reminders(
            file,
            reminders,
            config.get("listHeaderLevel", 3),
            reminder_list,
            config["dateFormat"],
            config["timeFormat"],
            config["dateTimeSeparator"],
            config.get("wrapDateStringInInternalLink", False),
        )
