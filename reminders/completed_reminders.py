# ios_reminders_to_markdown_journal/reminders/completed_reminders.py

from Foundation import NSDate
from EventKit import EKEventStore, EKEntityTypeReminder
from datetime import datetime
from database import (
    get_tags_for_reminder,
    get_url_for_reminder,
    add_section_to_reminders,
    find_parent_reminder,
)
from .tag_extractor import extract_hashtags_from_notes
from config import config


def get_completed_reminders_for_list(list_names, start_date=None, end_date=None):
    store = EKEventStore.alloc().init()
    store.requestAccessToEntityType_completion_(EKEntityTypeReminder, None)
    calendars = store.calendarsForEntityType_(EKEntityTypeReminder)

    target_calendars = [
        calendar for calendar in calendars if calendar.title() in list_names
    ]

    if not target_calendars:
        print(f"No lists found among: {', '.join(list_names)}")
        return {}

    predicate = store.predicateForRemindersInCalendars_(target_calendars)
    all_reminders = store.remindersMatchingPredicate_(predicate)

    completed_reminders_by_list = {list_name: [] for list_name in list_names}
    use_database = config.get("useDatabaseFunctions", True)

    for reminder in all_reminders:
        list_name = reminder.calendar().title()
        if list_name not in list_names:
            continue

        if reminder.isCompleted():
            completion_date = reminder.completionDate()
            creation_date = reminder.creationDate()

            if completion_date:
                completion_date = datetime.fromtimestamp(
                    completion_date.timeIntervalSince1970()
                )
                creation_date = datetime.fromtimestamp(
                    creation_date.timeIntervalSince1970()
                )

                if (start_date is None or completion_date.date() >= start_date) and (
                    end_date is None or completion_date.date() <= end_date
                ):
                    reminder_data = create_reminder_data(
                        reminder, completion_date, creation_date, use_database
                    )
                    completed_reminders_by_list[list_name].append(reminder_data)

    # Process parent-child relationships
    for list_name, reminders in completed_reminders_by_list.items():
        process_parent_child_relationships(reminders)

    # Add section information
    if use_database:
        for list_name, reminders in completed_reminders_by_list.items():
            calendar = next(
                (cal for cal in target_calendars if cal.title() == list_name), None
            )
            if calendar:
                completed_reminders_by_list[list_name] = add_section_to_reminders(
                    reminders, calendar.calendarIdentifier()
                )

    return completed_reminders_by_list


def create_reminder_data(reminder, completion_date, creation_date, use_database):
    # Extract notes and clean hashtags
    notes = reminder.notes()
    cleaned_notes, extracted_tags = extract_hashtags_from_notes(notes)

    reminder_data = {
        "name": reminder.title(),
        "body": cleaned_notes,  # Use cleaned notes without hashtags
        "creationDate": (
            creation_date.strftime("%Y-%m-%d %H:%M:%S") if creation_date else None
        ),
        "completionDate": (
            completion_date.strftime("%Y-%m-%d %H:%M:%S") if completion_date else None
        ),
        "allDayDueDate": reminder.dueDateAllDay(),
        "dueDate": (
            datetime.fromtimestamp(reminder.dueDate().timeIntervalSince1970()).strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            if reminder.dueDate()
            else None
        ),
        "priority": reminder.priority(),
        "UUID": reminder.calendarItemIdentifier(),
    }

    if use_database:
        # Get existing tags from database
        existing_tags = get_tags_for_reminder(reminder.calendarItemIdentifier())
        # Combine with extracted tags, ensuring no duplicates
        reminder_data["tags"] = list(set(existing_tags + extracted_tags))
        reminder_data["url"] = get_url_for_reminder(reminder.calendarItemIdentifier())
    else:
        reminder_data["tags"] = extracted_tags  # Just use extracted tags if no database
        reminder_data["url"] = None

    return reminder_data


def process_parent_child_relationships(reminders):
    # Create a mapping of UUID to reminder
    reminder_map = {reminder["UUID"]: reminder for reminder in reminders}

    for reminder in reminders:
        parent = find_parent_reminder(reminder["UUID"])
        if parent:
            reminder["parent_title"] = parent.get("title", "No title")
            reminder["parent_uuid"] = parent.get("uuid")

            # If the parent is not in our list of completed reminders, add it
            if parent["uuid"] not in reminder_map:
                parent_reminder = {
                    "UUID": parent["uuid"],
                    "name": parent["title"],
                    "completionDate": None,  # Parent task is not completed
                    "creationDate": reminder[
                        "creationDate"
                    ],  # Use child's creation date as an approximation
                    "body": "",
                    "tags": [],
                    "url": None,
                }
                reminders.append(parent_reminder)
                reminder_map[parent["uuid"]] = parent_reminder
        else:
            reminder["parent_title"] = None
            reminder["parent_uuid"] = None

    # Sort reminders to ensure parents come before children
    reminders.sort(
        key=lambda x: (
            x["parent_uuid"] is not None,
            x["completionDate"] or "9999-12-31",
        )
    )
