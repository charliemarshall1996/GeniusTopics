
def remove_new_line(input_string: str):
    """
    Remove new line and carriage return characters from the
    input string.

    Args:
    - `input_string` (`str`): The input string from which new
    line and carriage return 
        characters need to be removed.

    Returns:
    - `str`: The input string with new line and carriage return
    characters removed.
    """
    if not isinstance(input_string, str):
        return ""
    return input_string.replace("\n", "").replace("\r", "")
