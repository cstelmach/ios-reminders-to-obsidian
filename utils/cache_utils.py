import json
import os
from datetime import datetime, timedelta
from config import config

CACHE_FILE = "cache.json"


def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as file:
            cache = json.load(file)
    else:
        cache = {"last_extraction_date": None}
    return cache


def save_cache(last_extraction_date):
    with open(CACHE_FILE, "w") as file:
        json.dump(
            {"last_extraction_date": last_extraction_date.strftime("%Y-%m-%d")}, file
        )


def get_date_range():
    if not config["isCacheActive"]:
        start_date = datetime(1, 1, 1).date()  # very far in the past
    else:
        cache = load_cache()
        last_extraction_date = cache["last_extraction_date"]
        if last_extraction_date:
            start_date = datetime.strptime(
                last_extraction_date, "%Y-%m-%d"
            ).date() + timedelta(days=1)
        else:
            start_date = None  # Indicates that all reminders should be fetched
    end_date = (datetime.now() - timedelta(days=1)).date()
    return start_date, end_date


def update_cache():
    yesterday = (datetime.now() - timedelta(days=1)).date()
    save_cache(yesterday)
