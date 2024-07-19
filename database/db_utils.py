import sqlite3
import os
import glob
from config import config


def get_db_connection():
    manual_db_path = config.get("manualDatabaseFolderPath")
    if manual_db_path:
        db_glob_path = os.path.join(manual_db_path, "Data-*.sqlite")
    else:
        db_glob_path = os.path.expanduser(
            "~/Library/Group Containers/group.com.apple.reminders/Container_v1/Stores/Data-*.sqlite"
        )

    db_paths = glob.glob(db_glob_path)
    if not db_paths:
        raise FileNotFoundError("No SQLite database found for Reminders.")
    db_paths.sort(key=lambda x: os.path.getsize(x), reverse=True)
    db_path = db_paths[0]
    return sqlite3.connect(db_path)
