from .indentation_utils import write_multiline_text, write_multiline_body
from processing.task_utils import write_task_tags
from utils.datetime_formatter import format_date, format_time


def write_task(
    file,
    task,
    subtasks,
    date_format_for_datetime,
    time_format,
    separator,
    wrap_in_link,
    is_subtask=False,
):
    prefix = "\t" if is_subtask else ""
    checkbox = "[x]" if task["completionDate"] else "[-]"
    write_multiline_text(
        file, task["name"], prefix=prefix, initial_prefix=f"- {checkbox} "
    )

    if task.get("body") and task["body"] != "missing value":
        write_multiline_body(file, task["body"], prefix=prefix + "\t")

    formatted_creation_date = format_date(
        task["creationDate"], date_format_for_datetime, wrap_in_link
    )
    formatted_creation_time = format_time(task["creationDate"], time_format)
    formatted_completion_date = format_date(
        task["completionDate"], date_format_for_datetime, wrap_in_link
    )
    formatted_completion_time = format_time(task["completionDate"], time_format)

    file.write(
        f"{prefix}\t- created: {formatted_creation_date} {formatted_creation_time} -> completed: {formatted_completion_date} {formatted_completion_time}\n"
    )

    if task.get("url"):
        file.write(f"{prefix}\t- URL: {task['url']}\n")

    write_task_tags(file, task.get("tags", []), prefix=prefix)

    if subtasks:
        file.write(f"{prefix}\t- Subtasks:\n")
        for subtask in sorted(subtasks, key=lambda x: x["completionDate"]):
            write_task(
                file,
                subtask,
                [],
                date_format_for_datetime,
                time_format,
                separator,
                wrap_in_link,
                is_subtask=True,
            )

    file.write("\n")
