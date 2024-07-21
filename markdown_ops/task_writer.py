# ios_reminders_to_markdown_journal/markdown_ops/task_writer.py

from .indentation_utils import write_multiline_text, write_multiline_body
from processing.task_utils import write_task_tags
from .task_datetime_formatter import format_task_dates
from .task_property_formatter import format_task_properties, format_section_property
from config import config
from database.section_utils import should_hide_section


def get_checkbox_status(task, subtasks, parent_task=None):
    tag_dependent_completion_kinds = config.get("tagDependentCompletionKinds", {})
    section_dependent_completion_kinds = config.get(
        "sectionDependentCompletionKinds", {}
    )
    task_tags = set(task.get("tags", []))
    task_section = (
        task.get("section") or (parent_task.get("section") if parent_task else "") or ""
    )

    # Check for cancelled tags first (highest priority)
    cancelled_tags = set(tag_dependent_completion_kinds.get("cancelled", []))
    if task_tags.intersection(cancelled_tags):
        return config.get("cancelledCheckbox", "[~]")

    # Check for partially complete tags
    partially_complete_tags = set(
        tag_dependent_completion_kinds.get("partiallyComplete", [])
    )
    if task_tags.intersection(partially_complete_tags):
        return config.get("partiallyCompletedCheckbox", "[-]")

    # Check for cancelled sections (substring matching)
    cancelled_sections = section_dependent_completion_kinds.get("cancelled", [])
    if task_section and any(section in task_section for section in cancelled_sections):
        return config.get("cancelledCheckbox", "[~]")

    # Check for partially complete sections (substring matching)
    partially_complete_sections = section_dependent_completion_kinds.get(
        "partiallyComplete", []
    )
    if task_section and any(
        section in task_section for section in partially_complete_sections
    ):
        return config.get("partiallyCompletedCheckbox", "[-]")

    # If no tag or section dependent status, use the default logic
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
    parent_task=None,
):
    prefix = "\t" if is_subtask else ""

    checkbox = get_checkbox_status(task, subtasks, parent_task)

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

        # Write date string (creation/due/completion)
        date_string = format_task_dates(
            task, date_format_for_datetime, time_format, wrap_in_link
        )
        if date_string:
            file.write(f"{prefix}\t- {date_string}\n")

        # Format advanced properties
        format_single_line = config.get("formatAdvancedPropertiesInSingleLine", False)
        advanced_properties = []

        # Write additional task properties (including priority if it exists)
        properties = format_task_properties(task)
        advanced_properties.extend(properties)

        # Write section information if available and not hidden (only for main tasks and parent tasks)
        if (
            not is_subtask
            and task.get("section")
            and not should_hide_section(task["section"])
        ):
            section_string = format_section_property(task["section"])
            advanced_properties.append(section_string)

        # Write tags (now including tags from sections)
        tags_string = write_task_tags(task.get("tags", []), return_string=True)
        if tags_string:
            advanced_properties.append(tags_string)

        if advanced_properties:
            if format_single_line:
                file.write(f"{prefix}\t- {', '.join(advanced_properties)}\n")
            else:
                for prop in advanced_properties:
                    file.write(f"{prefix}\t- {prop}\n")

    if subtasks:
        file.write(f"{prefix}\t- Subtasks:\n\n")

        for index, subtask in enumerate(
            sorted(subtasks, key=lambda x: x.get("completionDate") or "9999-12-31")
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
                    parent_task=task,
                )
                # Don't print a new line after the last subtask
                if index < len(subtasks) - 1:
                    file.write("\n")

    if not is_subtask:
        file.write("\n")  # Add a new line after the main task
