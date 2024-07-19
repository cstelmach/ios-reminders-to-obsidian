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

    # Sort main tasks by completion date
    sorted_main_tasks = sorted(main_tasks.values(), key=lambda x: x["completionDate"])

    for task in sorted_main_tasks:
        write_task(
            file,
            task,
            child_tasks_by_parent_uuid.get(task["UUID"], []),
            date_format_for_datetime,
            time_format,
            separator,
            wrap_in_link,
        )

    # Process orphaned child tasks
    orphaned_child_tasks = [
        task
        for tasks in child_tasks_by_parent_uuid.values()
        for task in tasks
        if task["parent_uuid"] not in main_tasks
    ]
    if orphaned_child_tasks:
        file.write("\n### Orphaned Subtasks\n")
        for task in sorted(orphaned_child_tasks, key=lambda x: x["completionDate"]):
            write_task(
                file,
                task,
                [],
                date_format_for_datetime,
                time_format,
                separator,
                wrap_in_link,
                is_subtask=True,
            )
