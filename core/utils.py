import re
from unidecode import unidecode
from core import models


def normalize_name(name):
    """
    Normalize a name for comparisons between datasets.

    Punction and spaces are removed, non-US-ASCII characters are transliterated
    to the closest equivalent, and the result is uppercased.

    :param str name: Name as entered
    :rtype: str
    """
    char_regex = re.compile("[^a-zA-Z]")
    return char_regex.sub("", unidecode(name)).upper()


def p_transposed(first_name, last_name, gender=None, verbose=False):
    """
    Return probability that the name is transposed.

    From
    http://www2.census.gov/topics/genealogy/2000surnames/surnames.pdf#12
    """
    first_name_norm = normalize_name(first_name)
    first_name_counts = models.USName.query.get(first_name_norm)
    if first_name_counts:
        if gender == "M":
            first_name_1s = first_name_counts.count_given_male
        elif gender == "F":
            first_name_1s = first_name_counts.count_given_female
        else:
            first_name_1s = first_name_counts.count_given
        first_name_2m = first_name_counts.count_surname_male
        first_name_2f = first_name_counts.count_surname_female
    else:
        first_name_1s = 0
        first_name_2m = 0
        first_name_2f = 0

    last_name_norm = normalize_name(last_name)
    last_name_counts = models.USName.query.get(last_name_norm)
    if last_name_counts:
        if gender == "M":
            last_name_1s = last_name_counts.count_given_male
        elif gender == "F":
            last_name_1s = last_name_counts.count_given_female
        else:
            last_name_1s = last_name_counts.count_given
        last_name_2m = last_name_counts.count_surname_male
        last_name_2f = last_name_counts.count_surname_female
    else:
        last_name_1s = 0
        last_name_2m = 0
        last_name_2f = 0

    r_1 = (first_name_1s + 0.5) / (min(first_name_2m, first_name_2f) + 0.5)
    r_2 = (min(last_name_2m, last_name_2f) + 0.5) / (last_name_1s + 0.5)
    response = {
        "p_transposed": 1 - ((r_1 * r_2) / (1 + r_1 * r_2))
    }
    if verbose:
        response["first_normalized"] = normalize_name(first_name)
        response["last_normalized"] = normalize_name(last_name)
    return response
