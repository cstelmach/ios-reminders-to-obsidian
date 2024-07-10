import subprocess
import json
import os

MODULE_PATH = "/Users/cs/local/code/python_modules/ios_reminders_to_markdown_journal"


def run_jxa_script(script_path, args=None):
    command = ["osascript", "-l", "JavaScript", script_path]
    if args:
        command.extend(args)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Error running JXA script: {stderr.decode('utf-8')}")
    return stdout.decode('utf-8')


def list_completed_reminders(test_list=None):
    # Path to the JXA scripts
    script_path_1 = os.path.join(MODULE_PATH, "get_all_reminder_lists.jxa")
    script_path_2 = os.path.join(MODULE_PATH, "get_completed_reminders.jxa")

    if not test_list:
        # Run the first JXA script to get all reminder lists
        print("Running JXA script to get all reminder lists...")
        lists_output = run_jxa_script(script_path_1)
        reminder_lists = json.loads(lists_output)
    else:
        reminder_lists = [test_list]

    # Debug: Print all reminder lists
    print("All reminder lists:")
    for reminder_list in reminder_lists:
        print(reminder_list)

    # Run the second JXA script to get completed reminders for each list
    all_completed_reminders = {}
    for reminder_list in reminder_lists:
        print(
            f"Running JXA script to get completed reminders for list: {reminder_list}..."
        )
        reminders_output = run_jxa_script(script_path_2, args=[reminder_list])
        # Debug: Print the raw output from the JXA script
        print(f"Raw output for list {reminder_list}: {reminders_output}")
        completed_reminders = json.loads(reminders_output)
        all_completed_reminders[reminder_list] = completed_reminders

    return all_completed_reminders


if __name__ == "__main__":
    test_list = "temp.crap"
    completed_reminders = list_completed_reminders(test_list=test_list)
    print(json.dumps(completed_reminders, indent=2))