def write_multiline_text(file, text, prefix="", initial_prefix="- [x] "):
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if line.isspace() or not line:
            line = "_"
        if i == 0:
            file.write(f"{prefix}{initial_prefix}{line}\n")
        else:
            file.write(f"{prefix}\t  {line}\n")


def write_multiline_body(file, body, prefix=""):
    lines = body.split("\n")
    for i, line in enumerate(lines):
        if i == 0:
            file.write(f"{prefix}- {line}\n")
        else:
            file.write(f"{prefix}  {line}\n")
