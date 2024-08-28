# ios_reminders_to_markdown_journal/processing/task_utils.py

from config import config


def format_tag(tag):
    if config.get("useMetadataFormattingForTags", False):
        return f"(taskTag:: {tag})"
    return tag


def write_task_tags(tags, prefix="", return_string=False):
    tags_to_hide = config.get("tags", {}).get("tagsToHide", [])
    filtered_tags = [tag for tag in tags if tag.strip() and tag not in tags_to_hide]

    if filtered_tags:
        formatted_tags = [format_tag(tag) for tag in filtered_tags]
        if formatted_tags:
            tag_string = f"tags: {', '.join(formatted_tags)}"
            if return_string:
                return tag_string
            else:
                file.write(f"{prefix}\t- {tag_string}\n")
    return ""
