# iOS Reminders Export to Markdown Journal python_modules

## Useful links:

- SQL DB Notes: https://gist.github.com/0xdevalias/ccc2b083ff58b52aa701462f2cfb3cc8#reminders-sqlite-coredata-models--tables

## Tasks

- [ ] Add a progress bar or at least a console log?

### Bugs

- [ ] skipNotesAlreadyImported doesn't work with multiple lists. Fix it.


### statuPostponed:

- [ ]  Feat:: Add section parameter to the sections dictionary of the data.json and it's default called listsWithSectionsAsSubheadings, which is by default empty and it's value is a list of list strings or regexes.
  If the regex or string matches to a list, then for those lists, for the sections of those lists, instead of adding them as property, create a further subheading, one level below the list heading, and put all the reminders of the respective section in there. 

  If there are other in this list that have no section, then let the section name all reminders that have no section be "Other".

  ```json
    "sections": {
      "sectionsToHide": ["Hidden Section", ".*_hidden"],
      "sectionsToAddAsTags": [[".*OBE.*", "OBE"]],
      "listsWithSectionsAsSubheadings": []
    },
  ```
 

- [ ] Feat: sort the reminders of the respective sections according to their completion time, as already done in the list for the main tasks and the subtask in their respective parent task

- [ ] Feat: is there a way to sort the sections according to their order?

- [ ] feat: also add parameter "sectionsToIgnoreTasks" to the data.json and it's default. It is by default empty. Where if a section in the sectionsToIgnoreTasks list value is matching exactly (no substring matching), then don't export the tasks with this section but continue with the next task.



### Maybe OBE:


- [ ] Fix multi liist import. Currently it doesn't work as it should.

I've slightly modified the main.py to test the functionality for mutliple list imports and it currently doesn't work as it should:


What is the problem is that when the first list is imported, it of course of course also generates the section header if it doesn't exist already. And thus when the second list is about to be imported, the section header is found and this note import is skipped. 

Could you maybe try to check before you write any markdown, before doing all the lists, if the section header exists or not. And if it exists, then skip the import of all reminders tasks from this day?




---

- [ ] OBE: Order the completed reminders by their completion date?


- [ ] OBE?: Take the settings from periodic notes plugin. OBE because better to have everything independently.

````
Enhance the functionailty of the program and the data.json and data_default.json functionality:

/Users/cs/local/code/python_modules/ios_reminders_to_markdown_journal/data_default.json:1
```json
{
    "obsidianSettingsPath": null,
    "usePeriodicNotesPlugin": false,
    "dailyNoteFolderOverwrite": null,
    "dailyNoteFilenameOverwrite": null,
    "dateFormat": "YYYY-MM-DD",
    "timeFormat": "HH:mm:SS",
    "dateTimeSeparator": " ",
    "listHeaderLevel": 3,
    "sectionHeader": "Completed Tasks",
    "sectionHeaderLevel": 2,
    "wrapDateStringInInternalLink": false
}
```

If obsidianSettingsPath is specified and usePeriodicNotesPlugin is true, then inside the path search for the subpath with the file ../plugins/periodic-notes/data.json. 
get the data from this  data.json file of the periodic-notes plugin. It will look like this:


```json
{ "key": "value",
  "daily": {
    "format": "[JD] YYYYMMDD",
    "folder": "journal/day",
    "template": "slipbox/resources/templates/RT Journal-Day.md",
    "enabled": true
  },
...}
```

If no dailyNoteFolderOverwrite, dailyNoteFilenameOverwrite are given, take the daily.format as the file name and the daily.folder as the target folder instead.

Also take the daily.template, which will specify a relative path of the parent of the obsidianSettingsPath, and will be the template you use for new markdown files, to which you append the completed reminders markdown.

Also add a templateOverwritePath, which if specified will take the markdown file specified in this absolute path as template instead. Default value is Null. 


````
