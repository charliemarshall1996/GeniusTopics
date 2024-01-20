import regex
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
from .data.vocab import vocab_stop_words, vocab_replacements

lemmatizer = WordNetLemmatizer()


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


def strip_punctuation(input_string: str):
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


def strip_white_space(input_string: str):
    pattern = regex.compile(r"\s{2,}")
    if not isinstance(input_string, str):
        return ""
    return regex.sub(pattern, ' ', input_string).strip()


def normalize_case(input_string: str):
    if not isinstance(input_string, str):
        return ""
    return input_string.casefold()


def strip_stop_words(input_string: str):
    if not isinstance(input_string, str):
        return ""
    input_list = input_string.split(' ')
    stop_words = stopwords.words('english')
    stop_word_removed_list = [
        word for word in input_list if word not in stop_words]
    stop_word_removed_list = [
        word for word in stop_word_removed_list if word not in vocab_stop_words]
    return " ".join(stop_word_removed_list)


def lemmatize(input_string: str):
    if not isinstance(input_string, str):
        return ""
    return lemmatizer.lemmatize(input_string)
