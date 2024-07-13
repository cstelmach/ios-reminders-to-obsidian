def get_header(level, text):
    return f"{'#' * level} {text}\n\n"


def write_section_header(file, section_header, section_header_level):
    file.write("\n\n")
    file.write(get_header(section_header_level, section_header))
