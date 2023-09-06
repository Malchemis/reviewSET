"""Useful functions for the reviewSET.py script."""

def obtain_string_from_list(list):
    """Obtain a string from a list of strings."""
    string = ''
    for item in list:
        string += item + ', '
    return string[:-2]    

def combine_keywords(keywords1, keywords2):
    """Combine two lists of keywords into a single list."""
    keywords = []
    for keyword in keywords1:
        if keyword not in keywords:
            keywords.append(keyword)
    for keyword in keywords2:
        if keyword not in keywords:
            keywords.append(keyword)
    return keywords

def obtain_keywords(dict_field, keyword):
    """Obtain the desired keywords (for example category) from the specified dictionary field."""
    keywords = []
    for field in dict_field:
        keywords.append(field[keyword])
    return keywords