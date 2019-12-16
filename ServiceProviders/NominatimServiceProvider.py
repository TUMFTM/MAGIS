#!/usr/bin/env python
"""Defines how a request to the Nominatim sub-service is handled.
"""

from ServiceProviders.ServiceProvider import ServiceProvider
from Config import MAGIS_config as cfg
from flask import jsonify
from Core.MAGIS_utils import Service, Service_type, ARBITRARY_CHOICE, ARBITRARY_CHOICE_NO_DEFAULT

__author__ = "Lennart Adenaw"
__copyright__ = "Copyright 2019, Chair of Automotive Technology TU Munich"
__credits__ = ["Lennart Adenaw", "Julian Kreibich", "Michael Wittmann", "Markus Lienkamp"]
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Lennart Adenaw"
__email__ = "lennart.adenaw@tum.de"
__status__ = "alpha"

class NominatimServiceProvider(ServiceProvider):

    def __init__(self):

        super().__init__()

        self.type = Service_type.WEBSERVICE

        # TODO: Common true/false interface for all service parameters and all services. Momentary situation "true"/"false" vs. "0"/"1" vs. "True"/"False"
        # TODO: Consistency check : E.g. only one of polygon_xx can be 1 at a time
        # TODO: Parameters that do not need to be set, but need to be set to a discrete value if set
        # TODO: Add documentation for each parameter
        self.all_opts = {

            "service": ["search.php", "lookup.php", "reverse.php"],
            # "format" : ["json", "html", "xml", "jsonv2", "geojson", "geocodejson"],\ # Always set to geojson for GISAPI
            "format": ["geojson"],
            "json_callback": [ARBITRARY_CHOICE, "html"],
            "accept_language": ["en", "de"],
            "addressdetails": ["0", "1"],
            "debug": ["0", "1"],
            "polygon_geojson": ["0", "1"],
            "polygon_kml": ["0", "1"],
            "polygon_svg": ["0", "1"],
            "polygon_text": ["0", "1"],
            "extratags": ["0", "1"],
            "namedetails": ["0", "1"],
            "q": ARBITRARY_CHOICE_NO_DEFAULT,
            "street": ARBITRARY_CHOICE_NO_DEFAULT,
            "city": ARBITRARY_CHOICE_NO_DEFAULT,
            "county": ARBITRARY_CHOICE_NO_DEFAULT,
            "state": ARBITRARY_CHOICE_NO_DEFAULT,
            "country": ARBITRARY_CHOICE_NO_DEFAULT,
            "postalcode": ARBITRARY_CHOICE_NO_DEFAULT,
            "countrycodes": [ARBITRARY_CHOICE_NO_DEFAULT],
            "viewbox": ARBITRARY_CHOICE_NO_DEFAULT,
            "bounded": ["0", "1"],
            "exclude_place_ids": ARBITRARY_CHOICE_NO_DEFAULT,
            "dedupe": ["0", "1"],
            "osm_ids": ARBITRARY_CHOICE_NO_DEFAULT,
            "osm_type": ["N", "W", "R"],
            "osm_id": ARBITRARY_CHOICE_NO_DEFAULT,
            "zoom": [str(x) for x in [18] + list(range(0, 18))],
            "limit": [str(x) for x in [10] + list(range(1, 10)) + list(range(11, 51))],
            "lat": ARBITRARY_CHOICE_NO_DEFAULT,
            "lon": ARBITRARY_CHOICE_NO_DEFAULT

        }

        self.service_opts = {

            Service.GEOCODING: ["format", "json_callback", "accept_language", "addressdetails", "debug", "extratags", "namedetails", "q", "countrycodes", "viewbox", "bounded", "exclude_place_ids", "limit", "dedupe", "street", "city", "county", "state", "country", "postalcode", "polygon_geojson", "polygon_kml", "polygon_svg", "polygon_text"],
            Service.REVERSE_GEOCODING: ["format", "json_callback", "accept_language", "addressdetails", "debug", "extratags", "namedetails", "polygon_geojson", "polygon_kml", "polygon_svg", "polygon_text", "osm_type", "osm_id", "lat", "lon", "zoom"],
            Service.LOOKUP: ["format", "json_callback", "accept_language", "addressdetails", "debug", "extratags", "namedetails", "osm_ids"],

        }

        self.services_strs = {

            Service.GEOCODING: "search.php",
            Service.REVERSE_GEOCODING: "reverse.php",
            Service.LOOKUP: "lookup.php"

            }

        self.translation_dict = {"language": "accept-language"}  # Any jargon translations that shall be applied to either options or their values (k: api v: internal)

        self.iniOptions()

    def getQuery(self, service):

        # Setting service opt
        self.setOpt("service", self.services_strs[service])

        # Assembling base query
        base_query = "{protocol}{host}:{port}/{service}?"
        base_query = base_query.format(protocol='http://', host=cfg.NOMINATIM_HOST, port=cfg.NOMINATIM_PORT, service=self.opts["service"])

        # Identifying relevant opts for the service
        relevant_opts = self.service_opts[service]

        # Generating parameter sub-queries
        for i, opt in enumerate(relevant_opts):

            if self.opts[opt] is not None:
                if i != 0:
                    base_query += "&"
                base_query += "{opt_name}={opt_value}".format(opt_name=opt, opt_value=self.opts[opt])

        query = base_query

        return query

    def loadData(self, data):

        if "lat" in data.keys() and data["lat"] is not None:
            # It is already ensured that lat and lon appear in pairs if they appear at all (see requestHandler)
            self.setOpt("lat", data["lat"][-1])
            self.setOpt("lon", data["lon"][-1])

    def postprocess(self, r):

        out = r.json()

        return jsonify(out)