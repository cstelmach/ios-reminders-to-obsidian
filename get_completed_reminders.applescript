-- File: /Users/cs/local/code/python_modules/ios_reminders_to_markdown_journal/get_completed_reminders.applescript

on run argv
    set listName to item 1 of argv
    log "Getting completed reminders for list: " & listName
    tell application "Reminders"
        set theList to list listName
        set completedReminders to {}
        repeat with aReminder in (every reminder of theList whose completed is true)
            set reminderName to name of aReminder
            set reminderBody to body of aReminder
            set reminderCreationDate to creation date of aReminder
            set reminderCompletionDate to completion date of aReminder
            set reminderAllDayDueDate to allday due date of aReminder
            set reminderDueDate to due date of aReminder
            set reminderPriority to priority of aReminder

            if reminderCompletionDate is missing value then
                set reminderCompletionDate to ""
            else
                set reminderCompletionDate to reminderCompletionDate as Çclass isotÈ as string
            end if

            if reminderAllDayDueDate is missing value then
                set reminderAllDayDueDate to ""
            else
                set reminderAllDayDueDate to reminderAllDayDueDate as Çclass isotÈ as string
            end if

            if reminderDueDate is missing value then
                set reminderDueDate to ""
            else
                set reminderDueDate to reminderDueDate as Çclass isotÈ as string
            end if

            set reminderInfo to "{ \"name\": \"" & reminderName & "\", " & Â
                "\"body\": \"" & reminderBody & "\", " & Â
                "\"creationDate\": \"" & (reminderCreationDate as Çclass isotÈ as string) & "\", " & Â
                "\"completionDate\": \"" & reminderCompletionDate & "\", " & Â
                "\"allDayDueDate\": \"" & reminderAllDayDueDate & "\", " & Â
                "\"dueDate\": \"" & reminderDueDate & "\", " & Â
                "\"priority\": \"" & reminderPriority & "\" }"
            set end of completedReminders to reminderInfo
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