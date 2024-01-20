
def remove_new_line(string: str):
    try:
        string = string.replace("\n", "")
        return string.replace("\r", "")
    except (TypeError, AttributeError):
        return ""
