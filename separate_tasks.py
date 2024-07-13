def separate_tasks(reminders):
    main_tasks = {
        reminder["UUID"]: reminder
        for reminder in reminders
        if not reminder.get("parent_uuid")
    }
    child_tasks = [reminder for reminder in reminders if reminder.get("parent_uuid")]
    return main_tasks, child_tasks