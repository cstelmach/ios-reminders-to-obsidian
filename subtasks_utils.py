from utils.datetime_formatter import format_date, format_time
from indentation_utils import write_multiline_text, write_multiline_body
from task_utils import write_task_tags  # Import the new function

def append_subtasks(
    file,
    subtasks,
    date_format_for_datetime,
    time_format,
    separator,
    wrap_in_link,
    indentation,
):
    file.write(f"{indentation}- Subtasks:\n")
    for subtask in subtasks:
        write_multiline_text(
            file, subtask["name"], prefix=indentation + "\t", initial_prefix="- [x] "
        )
        if subtask.get("body") and subtask["body"] != "missing value":
            write_multiline_body(file, subtask["body"], prefix=indentation + "\t\t")
        formatted_creation_date = format_date(
            subtask["creationDate"], date_format_for_datetime, wrap_in_link
        )
        formatted_creation_time = format_time(subtask["creationDate"], time_format)
        formatted_completion_date = format_date(
            subtask["completionDate"], date_format_for_datetime, wrap_in_link
        )
        formatted_completion_time = format_time(subtask["completionDate"], time_format)
        file.write(
            f"{indentation}\t\t- created: {formatted_creation_date} {formatted_creation_time} -> completed: {formatted_completion_date} {formatted_completion_time}\n"
        )
        
        # Write tags for subtask
        write_task_tags(file, subtask.get("tags", []))