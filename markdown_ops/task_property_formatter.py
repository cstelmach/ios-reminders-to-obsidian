# ios_reminders_to_markdown_journal/markdown_ops/task_property_formatter.py

import re
from config import config


def format_property(key, value, use_metadata_formatting=None):
    if use_metadata_formatting is None:
        use_metadata_formatting = config.get("useMetadataFormattingForDatetimes", False)

    if use_metadata_formatting:
        return f"[{key}:: {value}]"
    else:
        return f"{key}: {value}"


def get_priority_value(priority):
    if priority == 1:
        return "low"
    elif priority == 5:
        return "medium"
    elif priority == 9:
        return "high"
    else:
        return None


def format_task_properties(task):
    properties = []

    # Handle priority
    priority = task.get("priority")
    if priority not in [None, 0]:
        priority_value = get_priority_value(priority)
        if priority_value:
            use_metadata_formatting = config.get(
                "useMetadataFormattingForPriority", False
            )
            priority_string = format_property(
                "priority", priority_value, use_metadata_formatting
            )
            properties.append(priority_string)

    # Add other properties here in the future if needed

    return properties


def clean_section_name(section_name):
    if config.get("removeNonStandardCharactersFromSectionNames", False):
        # Remove non-alphanumeric characters (except spaces)
        cleaned_name = re.sub(r"[^a-zA-Z0-9 ]", "", section_name)
        # Remove leading and trailing whitespace
        cleaned_name = cleaned_name.strip()
        return cleaned_name
    return section_name


def format_section_property(section):
    cleaned_section = clean_section_name(section)
    use_metadata_formatting = config.get("useMetadataFormattingForSections", False)
    return format_property("section", cleaned_section, use_metadata_formatting)
