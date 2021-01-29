#!/usr/bin/env python
"""Defines how a request to the OSM Explorer sub-service is handled.
"""

from ServiceProviders.ServiceProvider import ServiceProvider
from flask import jsonify
import psycopg2
import geopandas as gpd
import json
import geojson
import pandas as pd
from Core.MAGIS_utils import Service, Service_type, ARBITRARY_CHOICE_NO_DEFAULT, ARBITRARY_CHOICE

__author__ = "Lennart Adenaw"
__copyright__ = "Copyright 2019, Chair of Automotive Technology TU Munich"
__credits__ = ["Lennart Adenaw", "Julian Kreibich", "Michael Wittmann", "Markus Lienkamp"]
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Lennart Adenaw"
__email__ = "lennart.adenaw@tum.de"
__status__ = "alpha"

class OSMexplorerServiceProvider(ServiceProvider):

    def _definebasequeries(self):
        self.NODES_BASE_QUERY = "SELECT * FROM {node_table_name} WHERE id = {id}"
        self.NODES_LIST_BASE_QUERY = "SELECT * FROM {node_table_name} WHERE id in ({ids})"
        self.WAYS_BASE_QUERY = "SELECT * FROM {way_table_name} WHERE id = {id}"
        self.RELATIONS_BASE_QUERY = "SELECT * FROM {relation_table_name} WHERE id = {id}"
        self.WAY_NODES_BASE_QUERY = "SELECT way_id FROM way_nodes WHERE node_id={id}"

    def __init__(self, cfg):

        # Initialize standard ServiceProvider attributes
        super().__init__(cfg)

        # Set own type to callable
        self.type = Service_type.CALLABLE

        # Define base queries for sql requests
        self._definebasequeries()

        # Establish database connetion
        self.con, self.server = self._establish_db_con()

        # TODO: Common true/false interface for all service parameters and all services. Momentary situation "true"/"false" vs. "0"/"1" vs. "True"/"False"
        # TODO: Consistency check
        # TODO: Parameters that do not need to be set, but need to be set to a discrete value if set
        # TODO: Add documentation for each parameter
        self.all_opts = {

            "service": ["osmexp"],
            "func": ["nodeid2geominfo", "wayid2geominfo", "wayid2nodes", "nodeid2ways", ARBITRARY_CHOICE],
            "id": ARBITRARY_CHOICE_NO_DEFAULT

        }

        self.service_opts = {

            Service.OSMEXP: ["func", "id"],

        }

        self.services_strs = {

            Service.OSMEXP: "osmexp"

            }

        self.translation_dict = {}  # Any jargon translations that shall be applied to either options or their values (k: api v: internal) # TODO: Test this

        self.iniOptions()

    def _establish_db_con(self):

        server = None
        database = self.cfg.OSM_EXPLORER_DB_NAME
        user = self.cfg.OSM_EXPLORER_DB_USER
        password = self.cfg.OSM_EXPLORER_DB_USER_PASSWORD
        host = self.cfg.OSM_EXPLORER_DB_HOST
        port = self.cfg.OSM_EXPLORER_DB_PORT


        try:
            con = psycopg2.connect(database=database, user=user,
                                   password=password, host=host, port=port)
        except:
            raise Exception("Could not establish a connection with the config-file provided")

        return con, server

    def exit_all(self, con, server):
        con.close()

        if server is not None:
            server.stop()

    def _nodeid2node(self, id):

        # TODO: get this working for lists of ids
        if type(id) == int:
            node_query = self.NODES_BASE_QUERY.format(node_table_name="nodes", id=id)
            node = gpd.GeoDataFrame.from_postgis(node_query, self.con, geom_col='geom')
        elif type(id) == list and all(isinstance(x, int) for x in id):
            node_query = self.NODES_LIST_BASE_QUERY.format(node_table_name="nodes", ids=str(id).replace("[", "").replace("]", ""))
            node = gpd.GeoDataFrame.from_postgis(node_query, self.con, geom_col='geom')
        else:
            raise Exception("Supplied id must be an integer or a list of integers")

        return node

    def nodeid2ways(self, id):

        try:
            id = int(id)
        except:
            raise Exception("Supplied id must be an integer")

        query = self.WAY_NODES_BASE_QUERY.format(id=id)

        ways = pd.read_sql(query, self.con)

        out = {}

        if not ways.empty:
            # ways = ways.to_dict()
            out["code"] = "Success"
            out["way_ids"] = list(ways["way_id"])
            # way = json.loads(pd.io.json.dumps(ways))
        else:
            out = {"code": "Error", "reason": "No such node id in database or no way associated with node"}

        return out



    def nodeid2geominfo(self, id):

        # TODO: Is this postprocessing?

        try:
            id = int(id)
        except:
            raise Exception("Supplied id must be an integer")

        node = self._nodeid2node(id)

        if not node.empty:
            # TODO: There has to be a more elegant way to do this
            node = geojson.Feature(geometry=node["geom"][0], properties=json.loads(pd.DataFrame(node).drop("geom", axis=1).iloc[0].to_json()))
            node["code"] = "Success"
        else:
            node = {"code": "Error", "reason": "No such node id in database"}

        if 'properties' in node.keys():

            properties = node['properties']

            if 'tags' in properties.keys():

                # Extract properties
                tags = properties['tags']
                raw_tags = tags

                # Remove escape characters, whitespaces and quotations
                tags = tags.replace("\"", "")
                tags = tags.replace("\\", "")
                tags = tags.replace(" ", "")

                # Split tags from one another
                tags = tags.split(sep=",")

                prepared_tags = tags

                # Parse tags to key value pairs
                try:
                    keyvalue = [kv.split(sep='=>') for kv in tags]
                    for i, kv in enumerate(keyvalue):
                        tags[i] = {kv[0]: kv[1]} if len(kv)==2 else {kv[0]:None}
                        # tags = [{kv[0]: kv[1]} for kv in keyvalue if len(kv)==2]
                except:
                    tags=None

                final_tags = {}

                for tag in tags:
                   final_tags = {**final_tags, **tag}

                properties['tags'] = final_tags
                properties['raw_tags'] = raw_tags
                # properties['prepared_tags'] = prepared_tags

                node['properties'] = properties

        return node

    def wayid2geominfo(self, id):

        con, server = self._establish_db_con()

        way = self.wayid2nodes(id)

        if way["code"] == "Success":

            nodes = way["nodes"]
            raw_tags = way["tags"]

            node_geominfo = []

            for node in nodes:
                node_geominfo.append(self.nodeid2geominfo(node))

            final_tags=raw_tags

            return {"way_id": id, "raw_way_tags": raw_tags, "way_tags": final_tags, "nodes": node_geominfo}

        else:

            return way


    def wayid2nodes(self, id):

        try:
            id = int(id)
        except:
            raise Exception("Supplied id must be an integer")

        if type(id) == int:
            way_query = self.WAYS_BASE_QUERY.format(way_table_name="ways", id=id)
            way = pd.read_sql(way_query, self.con)
        else:
            raise Exception("Supplied id must be an integer")

        # self.exit_all(con, server)

        if not way.empty:
            way = way.iloc[0].to_dict()
            way["code"] = "Success"
            way = json.loads(pd.io.json.dumps(way))

            if "tags" in way.keys() and way["tags"]:

                raw_tags = way["tags"]

                # Remove escape characters, whitespaces and quotations
                tags = raw_tags.replace("\"", "")
                tags = tags.replace("\\", "")
                tags = tags.replace(" ", "")

                # Split tags from one another
                tags = tags.split(sep=",")

                # Parse tags to key value pairs
                try:
                    keyvalue = [kv.split(sep='=>') for kv in tags]
                    for i, kv in enumerate(keyvalue):
                        tags[i] = {kv[0]: kv[1]} if len(kv) == 2 else {kv[0]: None}
                        # tags = [{kv[0]: kv[1]} for kv in keyvalue if len(kv)==2]
                except:
                    tags = None

                final_tags = {}

                for tag in tags:
                    final_tags = {**final_tags, **tag}

                way["raw_tags"] = raw_tags
                way["tags"] = final_tags

        else:
            way = {"code": "Error", "reason": "No such way id in database"}

        return way

    def process(self, service):

        out = {}

        if self.opts["id"] == ARBITRARY_CHOICE_NO_DEFAULT:
            # No id has been supplied

            out['code'] = 'Error'
            out['reason'] = 'No id has been supplied'

            return jsonify(out)

        if self.opts['func'] not in self.all_opts['func']:
            # An invalid function has been requested from the osm_explorer

            out['code'] = 'Error'
            out['reason'] = 'There is no function {func}'.format(func=self.opts['func'])

            return jsonify(out)

        else:

            if self.opts["func"] == "nodeid2geominfo":
                out = self.nodeid2geominfo(self.opts["id"])

            elif self.opts["func"] == "wayid2geominfo":
                out = self.wayid2geominfo(self.opts["id"])

            elif self.opts["func"] == "wayid2nodes":
                out = self.wayid2nodes(self.opts["id"])

            elif self.opts["func"] == "nodeid2ways":
                out = self.nodeid2ways(self.opts["id"])

            else:
                out = self.nodeid2geominfo(self.opts["id"])

            return jsonify(out)

    def close_connections(self):
        self.exit_all(self.con, self.server)

    def __del__(self):
        self.exit_all(self.con, self.server)