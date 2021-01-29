#!/usr/bin/env python
"""Defines how a request to the OSRM sub-service is handled.
"""

from ServiceProviders.ServiceProvider import ServiceProvider
from flask import jsonify
from Errors.MAGIS_error import MAGIS_error
from Core.MAGIS_utils import Service, Service_type, ARBITRARY_CHOICE_NO_DEFAULT, ARBITRARY_CHOICE, BOOL_CHOICE_FALSE_DEFAULT, BOOL_CHOICE_TRUE_DEFAULT
import json

__author__ = "Lennart Adenaw"
__copyright__ = "Copyright 2019, Chair of Automotive Technology TU Munich"
__credits__ = ["Lennart Adenaw", "Julian Kreibich", "Michael Wittmann", "Markus Lienkamp"]
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Lennart Adenaw"
__email__ = "lennart.adenaw@tum.de"
__status__ = "alpha"

class OSRMServiceProvider(ServiceProvider):

    def __init__(self, cfg):

        super().__init__(cfg)

        self.type = Service_type.WEBSERVICE

        # TODO: Common true/false interface for all service parameters and all services. Momentary situation "true"/"false" vs. "0"/"1" vs. "True"/"False"
        # TODO: Consistency check
        # TODO: Parameters that do not need to be set, but need to be set to a discrete value if set
        # TODO: Add documentation for each parameter
        self.all_opts = {

            "service": ["route", "nearest", "table", "match", "trip", "tile"],
            "bearings": ARBITRARY_CHOICE_NO_DEFAULT,
            "radiuses": ARBITRARY_CHOICE_NO_DEFAULT,
            "hints": ARBITRARY_CHOICE_NO_DEFAULT,
            "version": ["v1"],
            "profile": ["car", "bike", "foot"],
            "coordinates": ARBITRARY_CHOICE_NO_DEFAULT,
            "format": ["json"],
            "number": [1, ARBITRARY_CHOICE],
            "alternatives": BOOL_CHOICE_FALSE_DEFAULT,
            "steps": BOOL_CHOICE_FALSE_DEFAULT,
            "annotations": BOOL_CHOICE_TRUE_DEFAULT,
            # "geometries" : ["geojson", "polyline6", "polyline"] ,\ # Always set to geojson for GISAPI
            "geometries": ["geojson"],
            "overview": ["full", "simplified", "false"],
            "continue_straight": ["default", "true", "false"],
            "sources": ["all", ARBITRARY_CHOICE],
            "destinations": ["all", ARBITRARY_CHOICE],
            "timestamps": ARBITRARY_CHOICE_NO_DEFAULT

        }

        self.service_opts = {

            Service.ROUTING: ["alternatives", "steps", "annotations", "geometries", "overview", "continue_straight"],
            Service.NEAREST: ["number"],
            Service.TABLE: ["sources", "destinations"],
            Service.MAPMATCHING: ["steps", "geometries", "annotations", "overview", "timestamps", "radiuses"],
            Service.TRIP: ["steps", "annotations", "geometries", "overview"],
            Service.TILE: []

        }

        self.services_strs = {

            Service.ROUTING: "route",
            Service.NEAREST: "nearest",
            Service.TABLE: "table",
            Service.MAPMATCHING: "match",
            Service.TRIP: "trip",
            Service.TILE: "tile"

            }

        self.translation_dict = {}  # Any jargon translations that shall be applied to either options or their values (k: api v: internal) # TODO: Test this

        self.iniOptions()

    def getQuery(self, service):

        # Setting service opt
        self.setOpt("service", self.services_strs[service])

        self.parseData()

        # Assembling base query
        base_query = "{protocol}{host}:{port}/{service}/{version}/{profile}/{coordinates}?"
        base_query = base_query.format(protocol='http://', host=self.cfg.OSRM_HOST, port=self.cfg.OSRM_PORT, service=self.opts["service"], version=self.opts["version"], profile=self.opts["profile"], coordinates=self.opts["coordinates"])

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

    def parseData(self):

        if self.opts["coordinates"] is not None:
            coordinates = self.opts["coordinates"]
            if type(coordinates)==str:
                coordinates = json.loads(coordinates)

            points = ""

            for i, coordinate in enumerate(coordinates):
                points += "{},{}".format(coordinate[1], coordinate[0])
                if i!=len(coordinates)-1:
                    points+=";"

            self.setOpt("coordinates", points)

        else:
            return MAGIS_error.DATA_MISSING_COORDINATES_ERROR

        if self.opts["timestamps"] is not None:
            # If timestamps have been passed

            times = self.opts["timestamps"]

            time_str = ""

            for i, time in enumerate(times):

                if i != 0:
                    t_str = ";"
                else:
                    t_str = ""
                t_str += str(int(times[i].timestamp()))
                time_str += t_str

            self.setOpt("timestamps", time_str)

    def postprocess(self, r):

        out = r.json()

        if self.opts["service"] == "match" and self.opts["annotations"] == "true":

            if 'code' in out.keys() and out['code'] == 'Ok':

                matchings = out["matchings"]

                tracepoints = out['tracepoints']
                locations = []

                for tp in tracepoints:
                    if tp is not None and 'location' in tp.keys():
                        locations.append(tp['location'])

                #locations = [tp['location'] for tp in tracepoints]

                confidences = [matching['confidence'] for matching in matchings]
                legs = sum([matching['legs'] for matching in out["matchings"]], [])
                annotations = [leg['annotation'] for leg in legs]
                nodes = [annotation['nodes'] for annotation in annotations]
                nodes = sum(nodes, [])
                out = {"code": "Success", "confidences": confidences, "matched_locations": locations, "nodes": nodes}

            else:

                out['code'] = "Error"

        elif self.opts["service"] == "match" and self.opts["annotations"] == "false":

            if 'code' in out.keys() and out['code'] == 'Ok':

                out['code'] = "Success"

            else:

                out['code'] = "Error"

        elif self.opts["service"] == "route":

            if 'code' in out.keys() and out['code'] == 'Ok':

                out['code'] = "Success"

            else:

                out['code'] = "Error"

        out = out
        out = jsonify(out)

        return out