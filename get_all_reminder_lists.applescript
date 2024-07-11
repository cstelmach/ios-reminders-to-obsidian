-- File: /Users/cs/local/code/python_modules/ios_reminders_to_markdown_journal/get_all_reminder_lists.applescript

log "Getting all reminder lists..."
tell application "Reminders"
    set listNames to name of every list
end tell
log "Retrieved all reminder lists."
-- Convert AppleScript list to JSON string
set jsonList to "["
repeat with listName in listNames
    set jsonList to jsonList & "\"" & listName & "\","
end repeat
-- Remove the last comma and close the JSON array
set jsonList to text 1 thru -2 of jsonList & "]"
return jsonList