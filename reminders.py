import json
from applescript_runner import run_applescript

def get_all_reminder_lists():
    script_name = "get_all_reminder_lists.applescript"
    lists_output = run_applescript(script_name)
    return json.loads(lists_output)

def get_completed_reminders_for_list(reminder_list):
    script_name = "get_completed_reminders.applescript"
    reminders_output = run_applescript(script_name, args=[reminder_list])
    return json.loads(reminders_output)