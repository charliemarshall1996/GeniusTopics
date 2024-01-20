import regex


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


def strip_text_w_sq_brackets(input_string: str):
    """
    Strip text within square brackets from the input string.

    Args:
    - `input_string` (`str`): The input string from which to
    remove text within square brackets.

    Returns:
    - `str`: The input string with text within square brackets
    removed.
    """
    pattern = regex.compile(r'\[([^[\]]*+(?:(?R)[^[\]]*+)*)\]')
    if not isinstance(input_string, str):
        return ""
    return regex.sub(pattern, '', input_string)


def strip_punctuation(input_string):
    """
    Strip punctuation from the input string and return the modified string.

    Args:
    - `input_string` (`str`): The input string from which
    punctuation will be stripped.

    Returns:
    - `str`: The modified string with punctuation stripped.
    """
    pattern = regex.compile(r"[^\w\s]")
    if not isinstance(input_string, str):
        return ""
    return regex.sub(pattern, '', input_string)


def strip_white_space(input_string):
    pattern = regex.compile(r"\s{2,}")
    if not isinstance(input_string, str):
        return ""
    return regex.sub(pattern, ' ', input_string).strip()
