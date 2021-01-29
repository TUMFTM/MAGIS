#!/usr/bin/env python
"""Provides helper functions used throughout MAGIS
"""

from enum import Enum

__author__ = "Lennart Adenaw"
__copyright__ = "Copyright 2019, Chair of Automotive Technology TU Munich"
__credits__ = ["Lennart Adenaw", "Julian Kreibich", "Michael Wittmann", "Markus Lienkamp"]
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Lennart Adenaw"
__email__ = "lennart.adenaw@tum.de"
__status__ = "alpha"

# Helper function to create the inverse of a dictionary
def invert_dict(d):

    return dict((v, k) for k in d for v in d[k])


# Identify service from api tag in URL
def apitag2service(api_tag_str, dict):

    if api_tag_str in dict.keys():
        return dict[api_tag_str]
    else:
        return None


def liststring2list(list_str):

    list_str = list_str.strip()  # Get rid of leading and trailing whitespaces

    if not (list_str[0] == "[" and list_str[-1] == "]"):
        # It is not a list
        return None
    else:
        list_str = list_str[1:-1]  # Remove Brackets
        list = list_str.split(",")  # Split into elements
        list = [e for e in list if e != ""]
        list = parse_list_strings(list)

        return list


def parse_list_strings(list_of_strings):

    # Try to parse elements
    for i, element in enumerate(list_of_strings):

        try:
            element_float = float(element)
        except:
            element_float = None
            pass

        if element_float is not None:
            list_of_strings[i] = element_float

    return list_of_strings

# SERVICES
class Service(Enum):

    ROUTING = 1
    MAPMATCHING = 2
    GEOCODING = 3
    REVERSE_GEOCODING = 4
    NEAREST = 5
    # ISOCRHONE = 6
    LOOKUP = 7
    TABLE = 8
    TRIP = 9
    TILE = 10
    OSMEXP = 11

# SERVICE TYPES
class Service_type(Enum):

    WEBSERVICE = 1
    CALLABLE = 2


# OPTION TYPES # TODO: Rethink and complete this!
class Option(Enum):

    INI_FIRST = 1
    NOT_SET_DEFAULT = 2

# OPTION SETTINGS
BOOL_CHOICE_FALSE_DEFAULT = ["false", "true"]
BOOL_CHOICE_TRUE_DEFAULT = ["true", "false"]
ARBITRARY_CHOICE_NO_DEFAULT = [None]
ARBITRARY_CHOICE = None
DEFAULT_IND = 0