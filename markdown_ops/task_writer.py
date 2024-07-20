# ios_reminders_to_markdown_journal/markdown_ops/task_writer.py

from .indentation_utils import write_multiline_text, write_multiline_body
from processing.task_utils import write_task_tags
from .task_datetime_formatter import format_task_dates
from .task_property_formatter import format_task_properties, format_section_property
from config import config
from database.section_utils import should_hide_section


def get_checkbox_status(task, subtasks):
    tag_dependent_completion_kinds = config.get("tagDependentCompletionKinds", {})
    task_tags = set(task.get("tags", []))

    # Check for cancelled tags first
    cancelled_tags = set(tag_dependent_completion_kinds.get("cancelled", []))
    if task_tags.intersection(cancelled_tags):
        return config.get("cancelledCheckbox", "[~]")

    # If not cancelled, check for partially complete tags
    partially_complete_tags = set(
        tag_dependent_completion_kinds.get("partiallyComplete", [])
    )
    if task_tags.intersection(partially_complete_tags):
        return config.get("partiallyCompletedCheckbox", "[-]")

    # If no tag-dependent status, use the default logic
    if task.get("status") == "cancelled":
        return config.get("cancelledCheckbox", "[~]")
    elif task.get("completionDate"):
        return "[x]"
    elif subtasks and any(subtask.get("completionDate") for subtask in subtasks):
        return config.get("partiallyCompletedCheckbox", "[-]")
    else:
        return "[ ]"


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

    checkbox = get_checkbox_status(task, subtasks)

    write_multiline_text(
        file, task["name"], prefix=prefix, initial_prefix=f"- {checkbox} "
    )

    # Only write additional details if the task is fully completed or is a parent task with completed subtasks
    if task.get("completionDate") or (not is_subtask and subtasks):
        # Combine body and URL
        body = task.get("body") or ""
        url = task.get("url")
        if url:
            body = f"{body}\n{url}" if body else url

        if body and body != "missing value":
            write_multiline_body(file, body, prefix=prefix + "\t")

        # Write additional task properties (including priority if it exists)
        properties = format_task_properties(task)
        for prop in properties:
            file.write(f"{prefix}\t- {prop}\n")

        # Write section information if available and not hidden (only for main tasks and parent tasks)
        if (
            not is_subtask
            and task.get("section")
            and not should_hide_section(task["section"])
        ):
            section_string = format_section_property(task["section"])
            file.write(f"{prefix}\t- {section_string}\n")

        # Write date string (creation/due/completion)
        date_string = format_task_dates(
            task, date_format_for_datetime, time_format, wrap_in_link
        )
        file.write(f"{prefix}\t- {date_string}\n")

        # Write tags (now including tags from sections)
        write_task_tags(file, task.get("tags", []), prefix=prefix)

    if subtasks:
        file.write(f"{prefix}\t- Subtasks:\n")
        for subtask in sorted(
            subtasks, key=lambda x: x.get("completionDate") or "9999-12-31"
        ):
            if subtask.get("completionDate"):
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
