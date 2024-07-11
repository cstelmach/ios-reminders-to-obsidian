import os

def check_section_header_exists(filepath, section_header, section_header_level):
    if not os.path.exists(filepath):
        return False
    with open(filepath, 'r') as file:
        content = file.read()
    header = f"\n{'#' * section_header_level} {section_header}\n"
    return header in content