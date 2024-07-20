import os


def get_header(level, text):
    return f"{'#' * level} {text}\n\n"


def write_export_header(file, export_header, export_header_level):
    file.write("\n\n")
    file.write(get_header(export_header_level, export_header))


def check_export_header_exists(filepath, export_header, export_header_level):
    if not os.path.exists(filepath):
        return False
    with open(filepath, "r") as file:
        content = file.read()
    header = f"\n{'#' * export_header_level} {export_header}\n"
    return header in content
