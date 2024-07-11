-- File: /Users/cs/local/code/python_modules/ios_reminders_to_markdown_journal/get_completed_reminders.applescript

on run argv
    set listName to item 1 of argv
    log "Getting completed reminders for list: " & listName
    tell application "Reminders"
        set theList to list listName
        set completedReminders to {}
        repeat with aReminder in (every reminder of theList whose completed is true)
            set end of completedReminders to "{ \"title\": \"" & name of aReminder & "\", \"completedDate\": \"" & completion date of aReminder & "\" }"
        end repeat
    end tell
    log "Completed getting reminders for list: " & listName
    -- Convert AppleScript list to JSON string
    set jsonReminders to "["
    repeat with reminder in completedReminders
        set jsonReminders to jsonReminders & reminder & ","
    end repeat
    -- Remove the last comma and close the JSON array
    set jsonReminders to text 1 thru -2 of jsonReminders & "]"
    return jsonReminders
end run