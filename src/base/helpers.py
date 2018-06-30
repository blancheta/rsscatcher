import re


def slugify(string):
    """
    Slugify a string to use it as an identifier
    """

    clean_string = str.lower(
        string.replace('/', ' ').replace("'", '').
            replace(':', ' ').replace('.', ' ').replace(' ', '-')
    )

    clean_string = re.sub("\-+", "-", clean_string)

    return clean_string
