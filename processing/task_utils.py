def write_task_tags(file, tags):
    if tags:
        file.write(f"\t- tags: {', '.join(tags)}\n")
