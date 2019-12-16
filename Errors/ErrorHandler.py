#!/usr/bin/env python
"""Defines the way MAGIS handles errors and defines error messages for the different error types from GIS_error
"""

from Errors.MAGIS_error import MAGIS_error

__author__ = "Lennart Adenaw"
__copyright__ = "Copyright 2019, Chair of Automotive Technology TU Munich"
__credits__ = ["Lennart Adenaw", "Julian Kreibich", "Michael Wittmann", "Markus Lienkamp"]
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Lennart Adenaw"
__email__ = "lennart.adenaw@tum.de"
__status__ = "alpha"

class ErrorHandler:

    def __init__(self):

        self.error_enum = MAGIS_error

        # Supply error messages or functions to be executed upon error
        self.error_hdl_dict = {

            MAGIS_error.DATA_PARSE_ERROR: "Could not parse supplied data! Please check supplied data format",
            MAGIS_error.DATA_TIME_PARSE_ERROR: "Error occured during parsing of supplied time stamps. Please make sure that timestamps are supplied in the following format: YYYY-MM-DD HH:MM:SS",
            MAGIS_error.DATA_CORRUPTED_COORDINATES_ERROR: "The number of latitude and longitude values does not match!",
            MAGIS_error.DATA_MISSING_COORDINATES_ERROR: "Not enough coordinates where supplied!",
            MAGIS_error.DATA_INCOMPATIBLE_TIME_NUM_ERROR: "The number of supplied timestamps is unequal to the number of supplied coordinates",
            MAGIS_error.HTTP_UNKNOWN_REQUEST_METHOD: "Please only access MAGIS via http GET or http POST"

            }

    def handle(self, err, err_data):

        out = self.error_hdl_dict[err]

        # If the error_hdl_dict contains a function for this error type, execute the function with the err_data
        if callable(out):
            out = out(err_data)

        return out

