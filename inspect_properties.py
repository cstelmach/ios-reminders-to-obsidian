import json
from applescript_runner import run_applescript

def inspect_reminder_properties():
    script_name = "inspect_reminder_properties.applescript"
    props_output = run_applescript(script_name)
    return json.loads(props_output)

if __name__ == "__main__":
    properties = inspect_reminder_properties()
    print(json.dumps(properties, indent=2))