#!/usr/bin/env python
"""Organizes the information flow from and to the MAGIS sub-services
"""

from ServiceProviders.NominatimServiceProvider import NominatimServiceProvider
from ServiceProviders.OSRMServiceProvider import OSRMServiceProvider
import requests
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

    def handle(self, request, service):

        # Merge dictionaries of json payload and arguments
        if request.json is not None and request.args:
            # Merging is necessary. Convert ImmutableMultiDict request.args to dict and merge with request.json
            request_dict = request.args.to_dict().update(request.json)
        else:
            # Either request.args or request.json is empty, use the one with data if any has data
            request_dict = request.args.to_dict() if request.args.to_dict() else request.json

        # Fetch suitable serviceRequest type
        service_provider = self.handle_dict[service]

        # Set up serviceProvider
        service_provider.loadRequest(request_dict)

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

    def _error_return(self, err_flag, err_data, data_dim=2):

        if data_dim == 1:
            return None, err_flag, err_data
        else:
            return None, None, err_flag, err_data