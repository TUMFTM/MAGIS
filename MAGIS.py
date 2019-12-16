#!/usr/bin/env python
"""Main part of the MAGIS reference implementation, routes all requests from the server to the subservices and organizes the program structure
"""

from flask import Flask, request, redirect
from Core.RequestHandler import RequestHandler
from Core.MAGIS_utils import apitag2service, SERVICES_DICT_INV, DOC_REROUTE_DICT
from Config import MAGIS_config as cfg
from Errors.ErrorHandler import ErrorHandler
from Errors.MAGIS_error import MAGIS_error

__author__ = "Lennart Adenaw"
__copyright__ = "Copyright 2019, Chair of Automotive Technology TU Munich"
__credits__ = ["Lennart Adenaw", "Julian Kreibich", "Michael Wittmann", "Markus Lienkamp"]
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Lennart Adenaw"
__email__ = "lennart.adenaw@tum.de"
__status__ = "alpha"

# Create new flask API
app = Flask('MAGIS')

# Initialize error handler
error_handler = ErrorHandler()
# Todo: Create error object, which logs all errors that occured. Make it writeable from everywhere in the GISAPI rather than passing error flags and error data around


# Route index
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    # TODO : Beautify the index page
    return ("<html>Please choose a gis service. See the MAGIS documentation for reference : <a href='{}'>MAGIS Documentation</a></html>".format(cfg.DOC_LINK))


# Route services
@app.route('/<apiTag>', methods=['GET', 'POST'])
def serviceAPIRequest(apiTag):

    request_method = request.method

    # If the client issued a http-GET request
    if request_method == "GET":

        # Extract request arguments
        json = {}
        args = request.args

    # If the client issued a http-POST request
    elif request_method == "POST":

        # Extract request arguments and uploaded json data
        json = request.json
        args = request.args

    # If a protocol other than http-GET or http-POST was used by the client, throw an error
    else:
        return error_handler.handle(MAGIS_error.HTTP_UNKNOWN_REQUEST_METHOD, None)

    # Merge potentially uploaded json data and arguments to one dictionary in any case also transform from immutable dict to dict
    request_input = {**dict(json), **dict(args)}

    # Extract the requested api-tag (GIS service)
    apiTag_str = str(apiTag).lower()

    # Try to retrieve the correct MAGIS service
    service = apitag2service(apiTag_str, SERVICES_DICT_INV)

    # If there is no MAGIS service that goes by that name
    if service is None:
        # Google the inserted string for the user
        return redirect("http://lmgtfy.com/?q=" + apiTag_str, code=302)
    else:
        # Initialize a requestHandler object that handles the incoming request
        req_hdl = RequestHandler()

        # Extract geodata and options from the request_input dict. Store errors that eventually occur during extraction.
        # TODO: Only extract data necessary for the service
        data, options, err_flag, err_data = req_hdl.extractData(request_input)

        # If data and options where extracted correctly (no error appeared):
        if not err_flag:
            out = req_hdl.handle(options, data, service=service)
        else:
            out = error_handler.handle(err_flag, err_data)

    return out


# Route documentation
@app.route('/<apiTag>/doc', methods=['GET', 'POST'])
def doc(apiTag):

    apiTag_str = str(apiTag).lower()

    service = apitag2service(apiTag_str, dict=SERVICES_DICT_INV)

    if service is not None:
        return redirect(DOC_REROUTE_DICT[service], code=302)
    else:
        return redirect("http://lmgtfy.com/?q="+apiTag, code=302)


# Execute this when the MAGIS.py-script is run from a terminal
if __name__ == '__main__':
    # Startup flask server
    app.run(debug=True, host=cfg.MAGIS_HOST, port=cfg.MAGIS_PORT)

