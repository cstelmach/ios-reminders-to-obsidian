-- File: /Users/cs/local/code/python_modules/ios_reminders_to_markdown_journal/inspect_reminder_properties.applescript

tell application "Reminders"
    -- Get a sample reminder from the first list
    set theList to first list
    set theReminder to first reminder of theList
    -- Get all properties of the reminder
    set propertiesList to properties of theReminder
end tell

-- Convert AppleScript record to JSON string
set jsonProps to "{"
repeat with theProperty in propertiesList
    set propName to name of theProperty
    set propValue to value of theProperty
    set jsonProps to jsonProps & "\"" & propName & "\": \"" & propValue & "\","
end repeat
-- Remove the last comma and close the JSON object
set jsonProps to text 1 thru -2 of jsonProps & "}"
return jsonProps