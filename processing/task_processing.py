from .subtasks_utils import append_subtasks
from .task_utils import write_task_tags
from markdown_ops.indentation_utils import write_multiline_text, write_multiline_body
from utils.datetime_formatter import format_date, format_time
from config import config


def separate_tasks(reminders):
    if not config.get("useDatabaseFunctions", True):
        return reminders, []

    main_tasks = {
        reminder["UUID"]: reminder
        for reminder in reminders
        if not reminder.get("parent_uuid")
    }
    child_tasks = [reminder for reminder in reminders if reminder.get("parent_uuid")]
    return main_tasks, child_tasks


def group_child_tasks_by_parent(child_tasks):
    if not config.get("useDatabaseFunctions", True):
        return {}

    child_tasks_by_parent_uuid = {}
    for task in child_tasks:
        parent_uuid = task["parent_uuid"]
        if parent_uuid not in child_tasks_by_parent_uuid:
            child_tasks_by_parent_uuid[parent_uuid] = []
        child_tasks_by_parent_uuid[parent_uuid].append(task)
    return child_tasks_by_parent_uuid


def process_main_tasks(
    file,
    main_tasks,
    child_tasks_by_parent_uuid,
    date_format_for_datetime,
    time_format,
    separator,
    wrap_in_link,
):
    use_database = config.get("useDatabaseFunctions", True)

    if not use_database:
        for task in main_tasks:
            write_multiline_text(
                file,
                task["name"],
                prefix="",
                initial_prefix="- [x] ",
            )
            write_task_body_and_dates(
                file,
                task,
                date_format_for_datetime,
                time_format,
                wrap_in_link,
            )
            file.write("\n")
    else:
        for parent_uuid, parent_task in main_tasks.items():
            if parent_uuid in child_tasks_by_parent_uuid:
                parent_completed = parent_task["completionDate"] is not None
                parent_checkbox = "[x]" if parent_completed else "[-]"
                write_multiline_text(
                    file,
                    parent_task["name"],
                    prefix="",
                    initial_prefix=f"- {parent_checkbox} ",
                )

                if parent_completed:
                    write_task_body_and_dates(
                        file,
                        parent_task,
                        date_format_for_datetime,
                        time_format,
                        wrap_in_link,
                    )

                write_task_tags(file, parent_task.get("tags", []))

                append_subtasks(
                    file,
                    child_tasks_by_parent_uuid[parent_uuid],
                    date_format_for_datetime,
                    time_format,
                    separator,
                    wrap_in_link,
                    "\t",
                )
                file.write("\n")
            else:
                parent_completed = parent_task["completionDate"] is not None
                parent_checkbox = "[x]" if parent_completed else "[-]"
                write_multiline_text(
                    file,
                    parent_task["name"],
                    prefix="",
                    initial_prefix=f"- {parent_checkbox} ",
                )
                write_task_body_and_dates(
                    file,
                    parent_task,
                    date_format_for_datetime,
                    time_format,
                    wrap_in_link,
                )

                write_task_tags(file, parent_task.get("tags", []))

                file.write("\n")


def process_child_tasks_without_parent(
    file,
    child_tasks_by_parent_uuid,
    main_tasks,
    date_format_for_datetime,
    time_format,
    separator,
    wrap_in_link,
):
    if not config.get("useDatabaseFunctions", True):
        return

    for parent_uuid, subtasks in child_tasks_by_parent_uuid.items():
        if parent_uuid not in main_tasks:
            parent_checkbox = "[-]"
            parent_title = subtasks[0]["parent_title"]
            write_multiline_text(
                file, parent_title, prefix="", initial_prefix=f"- {parent_checkbox} "
            )
            append_subtasks(
                file,
                subtasks,
                date_format_for_datetime,
                time_format,
                separator,
                wrap_in_link,
                "\t",
            )
            file.write("\n")


def write_task_body_and_dates(
    file, task, date_format_for_datetime, time_format, wrap_in_link
):
    if task.get("body") and task["body"] != "missing value":
        write_multiline_body(file, task["body"], prefix="\t")
    formatted_creation_date = format_date(
        task["creationDate"], date_format_for_datetime, wrap_in_link
    )
    formatted_creation_time = format_time(task["creationDate"], time_format)
    formatted_completion_date = format_date(
        task["completionDate"], date_format_for_datetime, wrap_in_link
    )
    formatted_completion_time = format_time(task["completionDate"], time_format)
    file.write(
        f"\t- created: {formatted_creation_date} {formatted_creation_time} -> completed: {formatted_completion_date} {formatted_completion_time}\n"
    )
