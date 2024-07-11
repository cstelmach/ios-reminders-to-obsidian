import subprocess
import os

MODULE_PATH = "/Users/cs/local/code/python_modules/ios_reminders_to_markdown_journal"

def run_applescript(script_name, args=None):
    script_path = os.path.join(MODULE_PATH, script_name)
    command = ["osascript", script_path]
    if args:
        command.extend(args)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        raise Exception(f"Error running AppleScript: {stderr.decode('utf-8')}")
    return stdout.decode('utf-8').strip()