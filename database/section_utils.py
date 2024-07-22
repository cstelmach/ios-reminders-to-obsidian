# ios_reminders_to_markdown_journal/database/section_utils.py

import json
import re
from .db_utils import get_db_connection
from config import config


def get_sections_for_list(list_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Get the Z_PK for the list
        cursor.execute(
            "SELECT Z_PK FROM ZREMCDBASELIST WHERE ZCKIDENTIFIER = ?", (list_id,)
        )
        list_pk = cursor.fetchone()

        if not list_pk:
            return None

        list_pk = list_pk[0]

        # Get sections for the list
        cursor.execute(
            "SELECT ZCKIDENTIFIER, ZDISPLAYNAME FROM ZREMCDBASESECTION WHERE ZLIST = ?",
            (list_pk,),
        )
        sections = cursor.fetchall()

        # Create a dictionary of section_id: section_name
        section_dict = {
            section[0]: section[1]
            for section in sections
            if not should_hide_section(section[1])
        }

        return section_dict
    finally:
        conn.close()


def get_section_memberships(list_id):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT ZMEMBERSHIPSOFREMINDERSINSECTIONSASDATA FROM ZREMCDBASELIST WHERE ZCKIDENTIFIER = ?",
            (list_id,),
        )
        memberships_data = cursor.fetchone()

        if not memberships_data or not memberships_data[0]:
            return None

        memberships_json = json.loads(memberships_data[0])

        # Create a dictionary of reminder_id: section_id
        memberships_dict = {
            m["memberID"]: m["groupID"] for m in memberships_json["memberships"]
        }

        return memberships_dict
    finally:
        conn.close()


def get_section_for_reminder(reminder_uuid, list_id):
    sections = get_sections_for_list(list_id)
    memberships = get_section_memberships(list_id)

    if not sections or not memberships:
        return None

    section_id = memberships.get(reminder_uuid)
    if not section_id:
        return None

    return sections.get(section_id)


def add_section_to_reminders(reminders, list_id):
    for reminder in reminders:
        if not reminder.get(
            "parent_uuid"
        ):  # Only add section to main tasks and parent tasks
            section = get_section_for_reminder(reminder["UUID"], list_id)
            reminder["section"] = section
            if section:
                tags_to_add = get_tags_for_section(section)
                reminder["tags"] = list(set(reminder.get("tags", []) + tags_to_add))
    return reminders


def should_hide_section(section_name):
    sections_to_hide = config.get("sectionsToHide", [])
    return any(
        (isinstance(pattern, str) and pattern == section_name)
        or (hasattr(pattern, "match") and pattern.match(section_name))
        for pattern in sections_to_hide
    )


def get_tags_for_section(section_name):
    sections_to_add_as_tags = config.get("sectionsToAddAsTags", [])
    tags = []
    for section_tag_config in sections_to_add_as_tags:
        if section_tag_config["sectionMatchRegex"].match(section_name):
            tags.append(section_tag_config["tagToAddUponMatch"])
    return tags
