from database import find_parent_reminder as db_find_parent_reminder


def find_parent_reminder(reminder_uuid):
    return db_find_parent_reminder(reminder_uuid)


# Add any other reminder-specific operations here
