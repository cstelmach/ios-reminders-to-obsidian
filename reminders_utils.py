from header_utils import get_header
from separate_tasks import separate_tasks
from group_child_tasks import group_child_tasks_by_parent
from process_main_tasks import process_main_tasks
from process_child_tasks_without_parent import process_child_tasks_without_parent

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

    process_main_tasks(
        file,
        main_tasks,
        child_tasks_by_parent_uuid,
        date_format_for_datetime,
        time_format,
        separator,
        wrap_in_link,
    )
    process_child_tasks_without_parent(
        file,
        child_tasks_by_parent_uuid,
        main_tasks,
        date_format_for_datetime,
        time_format,
        separator,
        wrap_in_link,
    )