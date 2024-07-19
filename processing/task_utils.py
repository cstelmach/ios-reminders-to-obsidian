def write_task_tags(file, tags, prefix=""):
    if tags:
        file.write(f"{prefix}\t- tags: {', '.join(tags)}\n")
