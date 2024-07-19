import re
from config import config


def filter_reminder_lists(all_reminder_lists):
    import_but_all_overwrite = config.get("importButAllOverwrite", False)
    lists_to_import = config.get("listsToImport", [])
    lists_to_omit = config.get("listsToOmit", [])

    filtered_lists = []
    for reminder_list in all_reminder_lists:
        list_title = reminder_list["title"]

        # Check if the list should be omitted
        if should_omit_list(list_title, lists_to_omit):
            continue

        # If importButAllOverwrite is True, include all lists except those in listsToOmit
        if import_but_all_overwrite:
            filtered_lists.append(list_title)
        # Otherwise, only include lists specified in listsToImport
        elif should_import_list(list_title, lists_to_import):
            filtered_lists.append(list_title)

    return filtered_lists


def should_omit_list(list_title, lists_to_omit):
    return any(match_pattern(list_title, pattern) for pattern in lists_to_omit)


def should_import_list(list_title, lists_to_import):
    return any(match_pattern(list_title, pattern) for pattern in lists_to_import)


def match_pattern(list_title, pattern):
    if isinstance(pattern, str):
        return pattern == list_title
    elif hasattr(pattern, "match"):  # Check if it's a regex object
        return pattern.match(list_title)
    else:
        try:
            return re.match(pattern, list_title)
        except re.error:
            print(f"Invalid regex pattern: {pattern}")
            return False
