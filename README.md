# iOS Reminders to Markdown Journal

## Overview

This program exports completed iOS Reminders tasks to Markdown files. It is designed to integrate seamlessly with Obsidian, a popular note-taking application. The exported tasks are formatted and organized in Markdown, making it easy to maintain a journal or log of completed tasks.

## Features

- **Export Completed Reminders**: Automatically export completed iOS Reminders tasks to Markdown files.
- **Obsidian Integration**: Optionally integrates with the Obsidian note-taking app using the Periodic Notes plugin.
- **Customizable Output**: Configure the output format, including date and time formats, headers, and templates.
- **Task Tags and URLs**: Extract and include task tags and URLs from the Reminders database.
- **Cache Mechanism**: Avoid reprocessing tasks that have already been exported.
- **Skip Already Imported Notes**: Skip days that have already been imported to avoid duplicates.

## Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/yourusername/ios_reminders_to_markdown_journal.git
   cd ios_reminders_to_markdown_journal
   ```

2. **Install Dependencies**
   Ensure you have Python and the required dependencies installed:
   ```sh
   pip install -r requirements.txt
   ```

## Configuration

The program uses a configuration file to customize its behavior. The configuration file should be named `data.json` and placed in the root directory of the project. A default configuration file (`data_default.json`) is provided.

### Configuration Options

- **obsidianSettingsPath**: Path to the Obsidian settings directory.
- **usePeriodicNotesPlugin**: Whether to use the Periodic Notes plugin for Obsidian.
- **dailyNoteFolderOverwrite**: Overwrite the folder where daily notes are saved.
- **dailyNoteFilenameOverwrite**: Overwrite the filename format for daily notes.
- **dateFormat**: Date format for task creation and completion dates.
- **timeFormat**: Time format for task creation and completion times.
- **dateTimeSeparator**: Separator between date and time.
- **listHeaderLevel**: Header level for the task list.
- **sectionHeader**: Section header for completed tasks.
- **sectionHeaderLevel**: Header level for the section header.
- **wrapDateStringInInternalLink**: Whether to wrap date strings in internal links.
- **templateOverwritePath**: Path to a custom template for new Markdown files.
- **isCacheActive**: Whether to use caching to avoid reprocessing tasks.
- **skipNotesAlreadyImported**: Whether to skip days that have already been imported.

### Example Configuration (`data.json`)

```json
{
  "obsidianSettingsPath": "/Users/cs/Obsidian/_/.obsidian",
  "usePeriodicNotesPlugin": true,
  "dailyNoteFolderOverwrite": "/Users/cs/local/code/python_modules/ios_reminders_to_markdown_journal",
  "dailyNoteFilenameOverwrite": "JD YYYYMMDD",
  "dateFormat": "JD YYYYMMDD",
  "timeFormat": "HH:mm",
  "dateTimeSeparator": " ",
  "listHeaderLevel": 3,
  "sectionHeader": "Completed Tasks",
  "sectionHeaderLevel": 2,
  "wrapDateStringInInternalLink": true,
  "templateOverwritePath": "/Users/cs/Obsidian/_/slipbox/resources/templates/RT Journal-Day-Only_Completed_Tasks.md",
  "isCacheActive": true,
  "skipNotesAlreadyImported": true
}
```

## Usage

1. **Run the Program**

   ```sh
   python main.py
   ```

2. **Optional Arguments**
   - `test_lists`: Pass a list of reminder lists to process specific lists.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
