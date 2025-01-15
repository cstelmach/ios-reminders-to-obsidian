import re


def extract_hashtags_from_notes(notes):
    """
    Extracts hashtags from notes and updates both the note content and tags list.

    Args:
        notes (str): The notes content from the reminder

    Returns:
        tuple: (cleaned_notes, extracted_tags) where:
            - cleaned_notes is the notes content with hashtags removed
            - extracted_tags is a list of extracted hashtag texts (without the # symbol)
    """
    if not notes or notes == "missing value":
        return "", []

    # Pattern matches hashtags that:
    # - start with a space or beginning of string (?:^|\s)
    # - followed by # symbol
    # - followed by one or more non-space characters (\S+)
    hashtag_pattern = r"(?:^|\s)#(\S+)"

    # Find all hashtags
    matches = re.finditer(hashtag_pattern, notes)
    extracted_tags = []
    end_positions = []

    # Extract tags and note positions
    for match in matches:
        tag = match.group(1)  # Get the tag without the # symbol
        extracted_tags.append(tag)
        # Store the start and end positions of the whole match (including space and #)
        end_positions.append((match.start(), match.end()))

    # If no hashtags found, return original notes
    if not extracted_tags:
        return notes, []

    # Remove hashtags from notes
    cleaned_notes = ""
    last_end = 0

    for start, end in end_positions:
        # Add text before the hashtag
        cleaned_notes += notes[last_end:start]
        last_end = end

    # Add remaining text after last hashtag
    cleaned_notes += notes[last_end:]

    # Clean up any resulting double spaces and trim
    cleaned_notes = re.sub(r"\s+", " ", cleaned_notes).strip()

    return cleaned_notes, extracted_tags
