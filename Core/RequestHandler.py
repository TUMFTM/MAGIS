#!/usr/bin/env python
"""Organizes the information flow from and to the MAGIS sub-services
"""

from datetime import datetime
from ServiceProviders.NominatimServiceProvider import NominatimServiceProvider
from ServiceProviders.OSRMServiceProvider import OSRMServiceProvider
import requests
from Errors.MAGIS_error import MAGIS_error
from ServiceProviders.OSMexplorerServiceProvider import OSMexplorerServiceProvider
from Core.MAGIS_utils import liststring2list, parse_list_strings
from Core.MAGIS_utils import Service, Service_type

__author__ = "Lennart Adenaw"
__copyright__ = "Copyright 2019, Chair of Automotive Technology TU Munich"
__credits__ = ["Lennart Adenaw", "Julian Kreibich", "Michael Wittmann", "Markus Lienkamp"]
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Lennart Adenaw"
__email__ = "lennart.adenaw@tum.de"
__status__ = "alpha"

class RequestHandler:

    def __init__(self, cfg):

        # This dictionary is used to map the services to instances of the corresponding request classes
        self.handle_dict = {

            Service.ROUTING: OSRMServiceProvider(cfg),
            Service.NEAREST: OSRMServiceProvider(cfg),
            Service.GEOCODING: NominatimServiceProvider(cfg),
            Service.REVERSE_GEOCODING: NominatimServiceProvider(cfg),
            Service.LOOKUP: NominatimServiceProvider(cfg),
            Service.MAPMATCHING: OSRMServiceProvider(cfg),
            #Service.OSMEXP: OSMexplorerServiceProvider(cfg)

            }

    def handle(self, options, data, service):

        # Fetch suitable serviceRequest type
        service_provider = self.handle_dict[service]

        # Set up serviceProvider
        service_provider.parseArgs(options)
        service_provider.loadData(data)

        # If the selected serviceProvider is a WEBSERVICE (i.e. a service that runs externally like Nominatim or OSRM)
        if service_provider.type == Service_type.WEBSERVICE:

            # Generate service query
            query = service_provider.getQuery(service)

            # Execute service query
            result = requests.get(query)

            # Save query and raw answer for debugging purposes
            with open("Logging/last_request_log.txt", "w+") as tmp:
                tmp.write("QUERY SENT TO SERVER:\n")
                tmp.write(query)
                tmp.write("\n\nSERVER RAW ANSWER:\n")
                tmp.write("Code: ")
                tmp.write(str(result.status_code))
                tmp.write("\nText: ")
                tmp.write(str(result.text))
                tmp.write("\nJSON: ")
                tmp.write(str(result.json()))

            # Perform postprocessing
            out = service_provider.postprocess(result)

        # If the selected serviceProvider is a CALLABLE (i.e. a MAGIS Python function)
        else:

            # process
            out = service_provider.process(service)

        return out

    def extractData(self, request_input):
        # TODO: It is not sensible to distinguish between data and options. Both will later be parsed into the options of specific requests. This should be changed

        data = None

        # Parse coordinates
        lats, lons, err_flag, err_data = self._request_input2coordinates(request_input)

        if not err_flag:
            # If there was no error so far..
            times, err_flag, err_data = self._request_input2times(request_input)

        if not err_flag:
            # If there was no error so far..
            options, err_flag, err_data = self._request_input2options(request_input)

        if not err_flag:
            # If there was no error so far..
            data = {"lat": lats, "lon": lons, "time": times}

        # TODO: Maybe the extraction routine should not care about lengths of the time list. There could be functions where time is used for sth else and does not have to fit the number of coordinates supplied
        if not err_flag:
            # If there was no error so far..
            if data["time"] is None or len(data["time"]) == len(data["lat"]):
                pass
            else:
                self._error_return(MAGIS_error.DATA_INCOMPATIBLE_TIME_NUM_ERROR, [len(data["time"]), len(data["lat"])])

        if err_flag:
            # If an error occured
            options = None
            data = None

        return data, options, err_flag, err_data

    def _error_return(self, err_flag, err_data, data_dim=2):

        if data_dim == 1:
            return None, err_flag, err_data
        else:
            return None, None, err_flag, err_data

    # Extract coordinate information from the request_input and make sure it is translated into a list of lats and a list of lons
    def _request_input2coordinates(self, request_input):

        lats = []
        lons = []

        err_flag = False
        err_data = None

        #############################################################################################
        # If coordinates have been supplied using the "coordinates"-tag
        #############################################################################################
        if "coordinates" in request_input.keys():

            coordinates = request_input["coordinates"]

            if type(coordinates)==list and len(coordinates)==1 and type(coordinates[0])==str:
                coordinates=coordinates[0]
                coordinates=liststring2list(coordinates)

            if type(coordinates) == list and all(isinstance(x, (int, float)) for x in coordinates):
                # If a list of coordinates has been supplied and all of these coordinates are either integers or floats

                if not len(coordinates) & 1 and len(coordinates) > 0:
                    # The number of supplied values is even, meaning there is a full set of 2-tuple coordinates
                    for i in range(len(coordinates)):
                        # Cut the coordinates list into lats and lons
                        if i & 1:
                            lats.append(coordinates[i])
                        else:
                            lons.append(coordinates[i])


                else:
                    # The number of supplied values is odd, meaning there is no full set of 2-tuple coordinates
                    return self._error_return(MAGIS_error.DATA_MISSING_COORDINATES_ERROR, None)

            else:
                # Data has been supplied using the coordinates tag, but this data contains values that are neither float nor integers
                return self._error_return(MAGIS_error.DATA_PARSE_ERROR, None)

        #############################################################################################
        # If coordinates have been supplied using the "lat"/"lon"-tag combination
        #############################################################################################
        elif "lat" in request_input.keys() or "lon" in request_input.keys():

            if "lat" and "lon" in request_input.keys():
                # Both, lats and lons have been supplied

                lats = request_input["lat"]
                lons = request_input["lon"]


                if len(lats) == 1 and type(lats[0]==str):

                    try:
                        # Try to interpret it as a float directly
                        lats = [float(lats[0])]
                    except:
                        # Try to interpret it as a list of floats, otherwise lats=None
                        lats = liststring2list(lats[0])

                if any(isinstance(x, (str)) for x in lats):
                    lats = parse_list_strings(lats)

                if len(lons) == 1 and type(lons[0])==str:

                    try:
                        #Try to interpret it as a float directly
                        lons = [float(lons[0])]
                    except:
                        # Try to interpret it as a list of floats, otherwise lons=None
                        lons = liststring2list(lons[0])

                if any(isinstance(x, (str)) for x in lons):
                    lons = parse_list_strings(lons)


                lats_intfloat_list_cond = type(lats)==list and all(isinstance(x, (int, float)) for x in lats)
                lons_intfloat_list_cond = type(lons) == list and all(isinstance(x, (int, float)) for x in lons)

                if lats_intfloat_list_cond and lons_intfloat_list_cond:
                    # Lat and lon values are supplied in list format and only contain integers and floats

                    if len(lats) == len(lons):
                        # Lats and lons have been supplied correctly
                        pass
                    else:
                        return self._error_return(MAGIS_error.DATA_MISSING_COORDINATES_ERROR, None)

                else:
                    # Data has been supplied using the coordinates tag, but this data contains values that are neither float nor integers
                    return self._error_return(MAGIS_error.DATA_PARSE_ERROR, None)

            else:
                # Only lats or lons have been supplied
                return self._error_return(MAGIS_error.DATA_MISSING_COORDINATES_ERROR, None)

        #############################################################################################
        # If no ccordinates have been supplied at all or if they have been supplied with an unknown tag
        #############################################################################################
        else:
            lats = None
            lons = None

        return lats, lons, err_flag, err_data

    # Extract time information from the request_input and make sure it is translated into a list of datetime objects
    def _request_input2times(self, request_input):

        times = []

        err_flag = False
        err_data = None

        if "time" in request_input.keys():
            # If timestamps have been supplied
            times = request_input["time"]

            if len(times) == 1 and type(times[0]) == str:
                times = liststring2list(times[0])

            # TODO: Maybe the extraction routing should not care about lengths of the time list. There could be functions where time is used for sth else and does not have to fit the number of coordinates supplied
            try:
                # Try to convert the time strings to the datetime format
                times = [datetime.strptime(i.strip(), "%Y-%m-%d %H:%M:%S") for i in times]
            except:
                # If the time conversion fails, throw an error
                return self._error_return(MAGIS_error.DATA_TIME_PARSE_ERROR, None, data_dim=1)

        else:

            times = None

        return times, err_flag, err_data

    # Extract all options from the request_input that are not coordinates or times
    def _request_input2options(self, request_input):

        data_tags = ["coordinates", "lat", "lon", "lats", "lons", "time", "times", "coordinates"]

        options = request_input
        options_keys = options.keys()
        options_keys = list(options_keys)  # Unlink options_keys from options.keys()

        # Remove keys that have already been handled during data extraction
        for key in options_keys:
            if key in data_tags:
                del options[key]
            else:
                options[key] = options[key][-1]

        return options, None, None