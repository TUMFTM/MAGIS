#!/usr/bin/env python
""" Parent class for all MAGIS sub-services.
"""

from Core.MAGIS_utils import invert_dict, DEFAULT_IND

__author__ = "Lennart Adenaw"
__copyright__ = "Copyright 2019, Chair of Automotive Technology TU Munich"
__credits__ = ["Lennart Adenaw", "Julian Kreibich", "Michael Wittmann", "Markus Lienkamp"]
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Lennart Adenaw"
__email__ = "lennart.adenaw@tum.de"
__status__ = "alpha"

class ServiceProvider:

    def __init__(self, cfg):

        self.cfg = cfg

        self.type = "serviceRequest"

        self.opts = {}
        self.all_opts = {}
        self.service_opts = {}

        self.translation_dict = {}

    def translateOpt(self, opt_name):

        translation_dict = invert_dict(self.translation_dict)

        if opt_name in list(translation_dict.keys()):
            return translation_dict[opt_name]
        else:
            return None

    def iniOptions(self):
        for opt in self.all_opts.keys():
            self.setOpt(opt, self.all_opts[opt][DEFAULT_IND])

    def setOpt(self, opt_name, val):

        opt_names = list(self.all_opts.keys())

        if opt_name in opt_names:

            valid_vals = self.all_opts[opt_name]
            arbitrary_val = None in valid_vals

            if val in valid_vals or arbitrary_val:
                self.opts[opt_name] = val

            return True

        return False

    def parseArgs(self, args):  # TODO: Test with lowercase and uppercase letters for every service

        # For each arg passed via MAGIS
        for arg in args.keys():
            # If there is a service option with the same name
            if arg in self.opts.keys():
                cur_opt = arg
            # If there is no service option with the same name, try to translate the name
            else:
                cur_opt = self.translateOpt(arg)

            self.setOpt(cur_opt, args[arg])

    def loadData(self, data):
        return "Implement me in sub-class"

    def getQuery(self, service):
        return "Implement me in sub-class if child is a webservice"

    def postprocess(self, r):
        return "Implement me in sub-class if child is a webservice"

    def process(self, service):
        return "Implement me in sub-class if child is a callable"