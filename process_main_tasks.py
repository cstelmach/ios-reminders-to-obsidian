from datetime_formatter import format_date, format_time
from indentation_utils import write_multiline_text, write_multiline_body
from subtasks_utils import append_subtasks
from task_utils import write_task_tags  # Import the new function

def process_main_tasks(
    file,
    main_tasks,
    child_tasks_by_parent_uuid,
    date_format_for_datetime,
    time_format,
    separator,
    wrap_in_link,
):
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
            
            # Write tags for parent task
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
            # If the parent task has no subtasks, just write the task
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
            
            # Write tags for parent task
            write_task_tags(file, parent_task.get("tags", []))
            
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