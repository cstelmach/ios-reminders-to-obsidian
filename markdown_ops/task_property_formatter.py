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
            priority_string = format_property("priority", priority_value)
            properties.append(priority_string)

    # Add other properties here in the future if needed

    return properties
