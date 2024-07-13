from datetime_formatter import format_date, format_time
from indentation_utils import write_multiline_text, write_multiline_body
from subtasks_utils import append_subtasks
from header_utils import get_header


def append_reminders(
    file,
    reminders,
    list_header_level,
    reminder_list,
    date_format_for_datetime,
    time_format,
    separator,
    wrap_in_link,
):
    file.write(get_header(list_header_level, reminder_list))
    parent_tasks = {}
    child_tasks = []

    for reminder in reminders:
        if reminder.get("parent_title"):
            if reminder["parent_title"] not in parent_tasks:
                parent_tasks[reminder["parent_title"]] = []
            parent_tasks[reminder["parent_title"]].append(reminder)
        else:
            child_tasks.append(reminder)

    for reminder in child_tasks:
        if reminder.get("name") and reminder["name"] != "missing value":
            write_multiline_text(file, reminder["name"])
        if reminder.get("body") and reminder["body"] != "missing value":
            write_multiline_body(file, reminder["body"], prefix="\t")
        if reminder.get("priority") and reminder["priority"] != 0:
            file.write(f"\t- priority: {reminder['priority']}\n")
        formatted_creation_date = format_date(
            reminder["creationDate"], date_format_for_datetime, wrap_in_link
        )
        formatted_creation_time = format_time(reminder["creationDate"], time_format)
        formatted_completion_date = format_date(
            reminder["completionDate"], date_format_for_datetime, wrap_in_link
        )
        formatted_completion_time = format_time(reminder["completionDate"], time_format)
        file.write(
            f"\t- created: {formatted_creation_date} {formatted_creation_time} -> completed: {formatted_completion_date} {formatted_completion_time}\n"
        )
        file.write("\n")

    for parent, subtasks in parent_tasks.items():
        parent_completed = all(subtask["completionDate"] for subtask in subtasks)
        parent_checkbox = "[x]" if parent_completed else "[-]"
        write_multiline_text(
            file, parent, prefix="", initial_prefix=f"- {parent_checkbox} "
        )
        formatted_creation_date = format_date(
            subtasks[0]["creationDate"], date_format_for_datetime, wrap_in_link
        )
        formatted_creation_time = format_time(subtasks[0]["creationDate"], time_format)
        if parent_completed:
            formatted_completion_date = format_date(
                subtasks[0]["completionDate"], date_format_for_datetime, wrap_in_link
            )
            formatted_completion_time = format_time(
                subtasks[0]["completionDate"], time_format
            )
            file.write(
                f"\t- created: {formatted_creation_date} {formatted_creation_time} -> completed: {formatted_completion_date} {formatted_completion_time}\n"
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
