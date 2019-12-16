#!/usr/bin/env python
"""Stores all possible Error Types of MAGIS
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

# make sure that the Error_handler class is able to handle all of these errors
class MAGIS_error(Enum):

    DATA_PARSE_ERROR = 1
    DATA_TIME_PARSE_ERROR = 2
    DATA_CORRUPTED_COORDINATES_ERROR = 3
    DATA_MISSING_COORDINATES_ERROR = 4
    DATA_INCOMPATIBLE_TIME_NUM_ERROR = 5
    HTTP_UNKNOWN_REQUEST_METHOD = 6