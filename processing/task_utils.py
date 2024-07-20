from config import config


def format_tag(tag):
    if config.get("useMetadataFormattingForTags", False):
        return f"(taskTag:: {tag})"
    return tag


def write_task_tags(file, tags, prefix=""):
    if tags:
        formatted_tags = ", ".join(format_tag(tag) for tag in tags)
        file.write(f"{prefix}\t- tags: {formatted_tags}\n")
