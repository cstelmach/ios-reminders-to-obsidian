from indentation_utils import write_multiline_text
from subtasks_utils import append_subtasks

def process_child_tasks_without_parent(
    file,
    child_tasks_by_parent_uuid,
    main_tasks,
    date_format_for_datetime,
    time_format,
    separator,
    wrap_in_link,
):
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