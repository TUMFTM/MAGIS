#!/usr/bin/env python
"""SHORT DESCRIPTION
"""

# Imports: 
import configparser
from configparser import ExtendedInterpolation
import json
from Core.MAGIS_utils import Service, invert_dict

__author__ = "Lennart Adenaw"
__copyright__ = "Copyright 2021, Chair of Automotive Technology TU Munich"
__credits__ = ["Lennart Adenaw", "Julian Kreibich", "Michael Wittmann", "Markus Lienkamp"]
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Lennart Adenaw"
__email__ = "lennart.adenaw@tum.de"
__status__ = "alpha"

class MAGISConfigReader:

    conf = None

    def __init__(self):
        pass

    def read(self, path, config_template_path=None):
        self.conf = self.__readConfigWithoutChecking(path)
        return MAGISConfig(self.conf), self.validateConfig(config_template_path)

    # TODO: Add reporting of missing config options
    def validateConfig(self, config_template_path):

        if config_template_path is None:
            return None
        else:
            template_config = self.__readConfigWithoutChecking(config_template_path)

        if self.conf.sections()!=template_config.sections():
            return False
        else:
            for section in template_config.sections():
                config_section = self.conf[section]
                template_config_section = template_config[section]
                if config_section.keys()!=template_config_section.keys():
                    return False

        return True

    def __readConfigWithoutChecking(self, path):
        conf = configparser.ConfigParser(interpolation = ExtendedInterpolation())
        conf.read(path)
        return conf

class MAGISConfig:

    def __init__(self, configparser_config):

        self.ONLY_GENERATE_STARTUP_SCRIPT = configparser_config["INSTALLATION_MODE"]["ONLY_GENERATE_STARTUP_SCRIPT"]

        self.SUB_GIS_INSTALLATION_BASE_PATH = configparser_config["DEPLOYMENT"]["SUB_GIS_INSTALLATION_BASE_PATH"]
        self.OSM_DATA_PATH = configparser_config["DEPLOYMENT"]["OSM_DATA_PATH"]

        self.MAGIS_PORT = int(configparser_config["DEPLOYMENT"]["MAGIS_PORT"])
        self.MAGIS_HOST = configparser_config["DEPLOYMENT"]["MAGIS_HOST"]

        self.NOMINATIM_HOST = configparser_config["DEPLOYMENT"]["NOMINATIM_HOST"]
        self.NOMINATIM_PORT = int(configparser_config["DEPLOYMENT"]["NOMINATIM_PORT"])
        self.NOMINATIM_PSQL_PORT = int(configparser_config["DEPLOYMENT"]["NOMINATIM_PSQL_PORT"])
        self.NOMINATIM_DB_USER = configparser_config["DEPLOYMENT"]["NOMINATIM_DB_USER"]
        self.NOMINATIM_DB_USER_PASSWORD = configparser_config["DEPLOYMENT"]["NOMINATIM_DB_USER_PASSWORD"]

        self.OSRM_HOST = configparser_config["DEPLOYMENT"]["OSRM_HOST"]
        self.OSRM_PORT = int(configparser_config["DEPLOYMENT"]["OSRM_PORT"])

        self.OSM_EXPLORER_DB_USER = configparser_config["DEPLOYMENT"]["OSM_EXPLORER_DB_USER"]
        self.OSM_EXPLORER_DB_USER_PASSWORD = configparser_config["DEPLOYMENT"]["OSM_EXPLORER_DB_USER_PASSWORD"]
        self.OSM_EXPLORER_DB_HOST = configparser_config["DEPLOYMENT"]["OSM_EXPLORER_DB_HOST"]
        self.OSM_EXPLORER_DB_NAME = configparser_config["DEPLOYMENT"]["OSM_EXPLORER_DB_NAME"]
        self.OSM_EXPLORER_DB_PORT = int(configparser_config["DEPLOYMENT"]["OSM_EXPLORER_DB_PORT"])

        self.OSM_SCHEMA = configparser_config["DEPLOYMENT"]["OSM_SCHEMA"]

        self.GUNICORN_PATH = configparser_config["DEPLOYMENT"]["GUNICORN_PATH"]

        # Service documentation links
        self.DOC_LINK = configparser_config["DOCUMENTATION"]["DOC_LINK"]
        self.ROUTE_DOC = configparser_config["DOCUMENTATION"]["ROUTE_DOC"]
        self.NEAREST_DOC = configparser_config["DOCUMENTATION"]["NEAREST_DOC"]
        self.ISOCHRONE_DOC = configparser_config["DOCUMENTATION"]["ISOCHRONE_DOC"]
        self.GEOCODING_DOC = configparser_config["DOCUMENTATION"]["GEOCODING_DOC"]
        self.REVERSE_GEOCODING_DOC = configparser_config["DOCUMENTATION"]["REVERSE_GEOCODING_DOC"]
        self.OSMEXP_DOC = configparser_config["DOCUMENTATION"]["OSMEXP_DOC"]
        self.LOOKUP_DOC = configparser_config["DOCUMENTATION"]["LOOKUP_DOC"]
        self.MAPMATCHING_DOC = configparser_config["DOCUMENTATION"]["MAPMATCHING_DOC"]
        self.TABLE_DOC = configparser_config["DOCUMENTATION"]["TABLE_DOC"]
        self.TRIP_DOC = configparser_config["DOCUMENTATION"]["TRIP_DOC"]
        self.TILE_DOC = configparser_config["DOCUMENTATION"]["TILE_DOC"]

        # SERVICES Parameters need to be parsed, because lists are expected
        self.whitelist_route = json.loads(configparser_config["ROUTING_ALIASES"]["whitelist_route"])
        self.whitelist_nearest = json.loads(configparser_config["ROUTING_ALIASES"]["whitelist_nearest"])
        # self.whitelist_isochrone = json.loads(configparser_config["ROUTING_ALIASES"]["whitelist_isochrone"])
        self.whitelist_geocode = json.loads(configparser_config["ROUTING_ALIASES"]["whitelist_geocode"])
        self.whitelist_reverse = json.loads(configparser_config["ROUTING_ALIASES"]["whitelist_reverse"])
        self.whitelist_lookup = json.loads(configparser_config["ROUTING_ALIASES"]["whitelist_lookup"])
        self.whitelist_mapmatch = json.loads(configparser_config["ROUTING_ALIASES"]["whitelist_mapmatch"])
        self.whitelist_table = json.loads(configparser_config["ROUTING_ALIASES"]["whitelist_table"])
        self.whitelist_trip = json.loads(configparser_config["ROUTING_ALIASES"]["whitelist_trip"])
        self.whitelist_tile = json.loads(configparser_config["ROUTING_ALIASES"]["whitelist_tile"])
        self.whitelist_osmexp = json.loads(configparser_config["ROUTING_ALIASES"]["whitelist_osmexp"])

        self.SERVICES_DICT = {

            Service.ROUTING: self.whitelist_route,
            Service.NEAREST: self.whitelist_nearest,
            Service.GEOCODING: self.whitelist_geocode,
            Service.REVERSE_GEOCODING: self.whitelist_reverse,
            Service.LOOKUP: self.whitelist_lookup,
            Service.MAPMATCHING: self.whitelist_mapmatch,
            Service.TILE: self.whitelist_tile,
            Service.TRIP: self.whitelist_trip,
            Service.TABLE: self.whitelist_table,
            Service.OSMEXP: self.whitelist_osmexp

        }

        self.SERVICES_DICT_INV = invert_dict(self.SERVICES_DICT)

        # DOCUMENTATION REROUTING
        self.DOC_REROUTE_DICT = {

            Service.ROUTING: self.ROUTE_DOC,
            Service.NEAREST: self.NEAREST_DOC,
            # Service.ISOCHRONE: cfg.ISOCHRONE,
            Service.GEOCODING: self.GEOCODING_DOC,
            Service.REVERSE_GEOCODING: self.REVERSE_GEOCODING_DOC,
            Service.LOOKUP: self.LOOKUP_DOC,
            Service.MAPMATCHING: self.MAPMATCHING_DOC,
            Service.TABLE: self.TABLE_DOC,
            Service.TRIP: self.TRIP_DOC,
            Service.TILE: self.TILE_DOC,
            Service.OSMEXP: self.OSMEXP_DOC

        }