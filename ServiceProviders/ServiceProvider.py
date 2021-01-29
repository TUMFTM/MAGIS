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

        else:
            self.opts[opt_name] = val

        return False

    def loadRequest(self, request_dict):

        # For each arg passed via MAGIS
        for arg in request_dict.keys():
            cur_opt = arg
            # If there is a service option with the same name
            if cur_opt  in self.opts.keys():
                pass
            # If there is no service option with the same name, try to translate the name, otherwise just keep it as it is
            else:
                if cur_opt in self.translation_dict.keys():
                    cur_opt = self.translateOpt(arg)
                else:
                    pass

            self.setOpt(cur_opt, request_dict[arg])

    def getQuery(self, service):
        return "Implement me in sub-class if child is a webservice"

    def postprocess(self, r):
        return "Implement me in sub-class if child is a webservice"

    def process(self, service):
        return "Implement me in sub-class if child is a callable"
