from .header_utils import write_section_header, get_header
from processing.task_processing import separate_tasks, group_child_tasks_by_parent
from .task_writer import write_task


def append_reminders_to_file(
    filename, reminders, section_header_exists, reminder_list, config
):
    with open(filename, "a") as file:
        if not section_header_exists:
            write_section_header(
                file, config["sectionHeader"], config["sectionHeaderLevel"]
            )
        else:
            file.write("\n")
        append_reminders(
            file,
            reminders,
            config.get("listHeaderLevel", 3),
            reminder_list,
            config["dateFormat"],
            config["timeFormat"],
            config["dateTimeSeparator"],
            config.get("wrapDateStringInInternalLink", False),
        )


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

    main_tasks, child_tasks = separate_tasks(reminders)
    child_tasks_by_parent_uuid = group_child_tasks_by_parent(child_tasks)

    # Combine main tasks and parent tasks of completed subtasks
    all_parent_tasks = {**main_tasks}
    for child_task in child_tasks:
        if child_task["parent_uuid"] not in all_parent_tasks:
            all_parent_tasks[child_task["parent_uuid"]] = {
                "UUID": child_task["parent_uuid"],
                "name": child_task["parent_title"],
                "completionDate": None,  # Parent task is not completed
            }

    # Sort all parent tasks by completion date, with incomplete tasks at the end
    sorted_parent_tasks = sorted(
        all_parent_tasks.values(), key=lambda x: x["completionDate"] or "9999-12-31"
    )

    for task in sorted_parent_tasks:
        write_task(
            file,
            task,
            child_tasks_by_parent_uuid.get(task["UUID"], []),
            date_format_for_datetime,
            time_format,
            separator,
            wrap_in_link,
        )
