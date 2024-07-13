# ios_reminders_to_markdown_journal/file_writer.py

from datetime_formatter import format_date, format_time


def get_header(level, text):
    return f"{'#' * level} {text}\n\n"


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
    for reminder in reminders:
        # do the same for the reminder name
        if reminder.get("name") and reminder["name"] != "missing value":
            title_lines = reminder["name"].split("\n")
            title_multi_line_prefix = ""

            if reminder.get("parent_title"):
                title_multi_line_prefix += "\t"

            for i, line in enumerate(title_lines):
                # if the line is empty or just spaces then replace it with "_"
                if line.isspace() or not line:
                    line = "_"
                if i == 0:
                    file.write(f"{title_multi_line_prefix}- [x] {line}\n")
                else:
                    file.write(f"{title_multi_line_prefix}\t  {line}\n")

        if reminder.get("body") and reminder["body"] != "missing value":
            # if the body contains multiple lines, then add a tab before each line
            # if the reminder has a parent, then add two tabs before each line
            # additionally the first line should have a "- " before the text, the others two spaces
            body_lines = reminder["body"].split("\n")
            body_multi_line_prefix = "\t"

            if reminder.get("parent_title"):
                body_multi_line_prefix += "\t"

            for i, line in enumerate(body_lines):
                if i == 0:
                    file.write(f"{body_multi_line_prefix}- {line}\n")
                else:
                    file.write(f"{body_multi_line_prefix}  {line}\n")

        if reminder.get("priority") and reminder["priority"] != 0:
            file.write(f"\t- priority: {reminder['priority']}\n")

        # Format creation date and time
        formatted_creation_date = format_date(
            reminder["creationDate"], date_format_for_datetime, wrap_in_link
        )
        formatted_creation_time = format_time(reminder["creationDate"], time_format)

        # Format completion date and time
        formatted_completion_date = format_date(
            reminder["completionDate"], date_format_for_datetime, wrap_in_link
        )
        formatted_completion_time = format_time(reminder["completionDate"], time_format)

        # Start building the date line
        date_line = f"\t- created: {formatted_creation_date} {formatted_creation_time}"

        # Add due date if present
        if reminder.get("dueDate") and reminder["dueDate"] != "missing value":
            formatted_due_date = format_date(
                reminder["dueDate"], date_format_for_datetime, wrap_in_link
            )
            if reminder.get("allDayDueDate"):
                date_line += f", due: {formatted_due_date}"
            else:
                formatted_due_time = format_time(reminder["dueDate"], time_format)
                date_line += f", due: {formatted_due_date} {formatted_due_time}"

        # Add completion date
        date_line += (
            f" -> completed: {formatted_completion_date} {formatted_completion_time}"
        )

        file.write(f"{date_line}\n")

        if reminder.get("parent_title"):
            file.write(f"\t- parent task: {reminder['parent_title']}\n")
        file.write("\n")


def write_section_header(file, section_header, section_header_level):
    file.write("\n\n")
    file.write(get_header(section_header_level, section_header))
