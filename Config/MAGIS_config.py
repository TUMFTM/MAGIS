#!/usr/bin/env python
"""Provides a configuration for MAGIS
"""

__author__ = "Lennart Adenaw"
__copyright__ = "Copyright 2019, Chair of Automotive Technology TU Munich"
__credits__ = ["Lennart Adenaw", "Julian Kreibich", "Michael Wittmann", "Markus Lienkamp"]
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Lennart Adenaw"
__email__ = "lennart.adenaw@tum.de"
__status__ = "alpha"

##############################
### INSTALLATION MODE      ###
##############################

ONLY_GENERATE_STARTUP_SCRIPT = False

##############################
### INSTALLATION / RUNTIME ###
##############################

# Target installation path
SUB_GIS_INSTALLATION_BASE_PATH = "/home/debian/MAGIS_sub_gis/"

# Input map data
OSM_DATA_PATH = "/home/debian/osm_data/monaco-latest.osm.pbf"

# Magis settings
MAGIS_PORT = 80
MAGIS_HOST = '127.0.0.1'

# Nominatim settings
NOMINATIM_HOST = '127.0.0.1'
NOMINATIM_PORT = "10011"
NOMINATIM_PSQL_PORT = 5432
NOMINATIM_DB_USER = "nominatim"
NOMINATIM_DB_USER_PASSWORD = "nominatim"

# OSRM settings
OSRM_HOST = '127.0.0.1'
OSRM_PORT = "5000"

# OSM explorer settings
OSM_EXPLORER_DB_USER= "osm_explorer"
OSM_EXPLORER_DB_USER_PASSWORD = "osm_explorer"
OSM_EXPLORER_DB_HOST = "localhost"
OSM_EXPLORER_DB_NAME = "osm"
OSM_EXPLORER_DB_PORT = 5432
OSM_EXPLORER_SSH_USER = ""
OSM_EXPLORER_SSH_USER_PASSWORD = ""
OSM_EXPLORER_USE_SSH = False

##############################
### DOCUMENTATION          ###
##############################

# General documentation link
DOC_LINK = "https://github.com/TUMFTM/MAGIS"

# Service documentation links
ROUTE_DOC = "https://github.com/TUMFTM/MAGIS"
NEAREST_DOC = "https://github.com/TUMFTM/MAGIS"
ISOCHRONE_DOC = "https://github.com/TUMFTM/MAGIS"
GEOCODING_DOC = "https://github.com/TUMFTM/MAGIS",
REVERSE_GEOCODING_DOC = "https://github.com/TUMFTM/MAGIS",
OSMEXP_DOC = "https://github.com/TUMFTM/MAGIS"
LOOKUP_DOC = "https://github.com/TUMFTM/MAGIS"
MAPMATCHING_DOC = "https://github.com/TUMFTM/MAGIS"
TABLE_DOC = "https://github.com/TUMFTM/MAGIS"
TRIP_DOC = "https://github.com/TUMFTM/MAGIS"
TILE_DOC = "https://github.com/TUMFTM/MAGIS"

##############################
### ROUTING ALIASES        ###
##############################

# SERVICES
whitelist_route = ["route", "routing"]
whitelist_nearest = ["nearest", "near", "close", "next"]
# whitelist_isochrone = ["isochrone", "iso-chrone","isochrones","iso-chrones"]
whitelist_geocode = ["geocoding", "geo-coding", "geocode", "search", "geo-code"]
whitelist_reverse = ["reverse", "reversegeocoding", "reversegeo-coding", "reverse-geo-coding", "re-verse"]
whitelist_lookup = ["lookup", "look-up"]
whitelist_mapmatch = ["mapmatching", "map-matching", "mapmatch", "map-match", "match"]
whitelist_table = ["table", "tables"]
whitelist_trip = ["trip", "trips"]
whitelist_tile = ["tile", "tiles"]
whitelist_osmexp = ["osm-explorer", "osmexplorer", "osm-exp", "osmexp"]