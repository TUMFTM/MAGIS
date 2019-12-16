#!/usr/bin/env python
"""Provides helper functions used throughout MAGIS
"""

from Config import MAGIS_config as cfg
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

    list_str = list_str.strip()  # Get rid of leading and traling whitespaces

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

# Service.ISOCRHONE: whitelist_isochrone,\
SERVICES_DICT = {

        Service.ROUTING: cfg.whitelist_route,
        Service.NEAREST: cfg.whitelist_nearest,
        Service.GEOCODING: cfg.whitelist_geocode,
        Service.REVERSE_GEOCODING: cfg.whitelist_reverse,
        Service.LOOKUP: cfg.whitelist_lookup,
        Service.MAPMATCHING: cfg.whitelist_mapmatch,
        Service.TILE: cfg.whitelist_tile,
        Service.TRIP: cfg.whitelist_trip,
        Service.TABLE: cfg.whitelist_table,
        Service.OSMEXP: cfg.whitelist_osmexp

    }

SERVICES_DICT_INV = invert_dict(SERVICES_DICT)

# SERVICE TYPES
class Service_type(Enum):

    WEBSERVICE = 1
    CALLABLE = 2


# OPTION TYPES # TODO: Rethink and complete this!
class Option(Enum):

    INI_FIRST = 1
    NOT_SET_DEFAULT = 2

# DOCUMENTATION REROUTING
DOC_REROUTE_DICT = {

            Service.ROUTING:  cfg.ROUTE_DOC,
            Service.NEAREST: cfg.NEAREST_DOC,
            # Service.ISOCHRONE: cfg.ISOCHRONE,
            Service.GEOCODING: cfg.GEOCODING_DOC,
            Service.REVERSE_GEOCODING: cfg.REVERSE_GEOCODING_DOC,
            Service.LOOKUP: cfg.LOOKUP_DOC,
            Service.MAPMATCHING: cfg.MAPMATCHING_DOC,
            Service.TABLE: cfg.TABLE_DOC,
            Service.TRIP: cfg.TRIP_DOC,
            Service.TILE: cfg.TILE_DOC,
            Service.OSMEXP:cfg.OSMEXP_DOC

        }

# OPTION SETTINGS
BOOL_CHOICE_FALSE_DEFAULT = ["false", "true"]
BOOL_CHOICE_TRUE_DEFAULT = ["true", "false"]
ARBITRARY_CHOICE_NO_DEFAULT = [None]
ARBITRARY_CHOICE = None
DEFAULT_IND = 0