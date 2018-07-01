import re


def slugify(string):
    """
    Slugify a string to use it as an identifier
    """

    clean_string = re.sub(r"\.+", "-", string)
    clean_string = re.sub(r"\:+", "-", clean_string)
    clean_string = re.sub(r"\'+", "-", clean_string)
    clean_string = re.sub(r"\/+", "-", clean_string)

    clean_string = re.sub(r"\-+", "-", clean_string)

    return clean_string
