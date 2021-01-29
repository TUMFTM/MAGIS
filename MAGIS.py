#!/usr/bin/env python
"""Main part of the MAGIS reference implementation, routes all requests from the server to the subservices and organizes the program structure
"""

from flask import Flask, request, redirect
from Core.RequestHandler import RequestHandler
from Core.MAGIS_utils import apitag2service
from Errors.ErrorHandler import ErrorHandler
from Errors.MAGIS_error import MAGIS_error
from Config.io import MAGISConfigReader
import os

__author__ = "Lennart Adenaw"
__copyright__ = "Copyright 2019, Chair of Automotive Technology TU Munich"
__credits__ = ["Lennart Adenaw", "Julian Kreibich", "Michael Wittmann", "Markus Lienkamp"]
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Lennart Adenaw"
__email__ = "lennart.adenaw@tum.de"
__status__ = "alpha"

def create_app():
    # Create new flask API
    app = Flask('MAGIS')

    # Load user configuration
    cfgReader = MAGISConfigReader()
    config_path = os.path.abspath("./Config/user/MAGIS_user_config.conf")
    os.system("echo Starting MAGIS within $PWD")
    os.system("echo Reading Config from {}".format(config_path))
    config, valid = cfgReader.read(os.path.abspath("./Config/user/MAGIS_user_config.conf"),
                                   config_template_path=os.path.abspath("./Config/MAGIS_config_template.conf"))

    if not valid:
        raise Exception("Please supply a user config matching the MAGIS_config_template.conf!")

    # Initialize error handler
    error_handler = ErrorHandler()

    # Route index
    @app.route('/', methods=['GET', 'POST'])
    @app.route('/index', methods=['GET', 'POST'])
    def index():
        # TODO : Beautify the index page
        return ("<html>Please choose a gis service. See the MAGIS documentation for reference : <a href='{}'>MAGIS Documentation</a></html>".format(config.DOC_LINK))


    # Route services
    @app.route('/<apiTag>', methods=['GET', 'POST'])
    def serviceAPIRequest(apiTag):

        # If a protocol other than http-GET or http-POST was used by the client, throw an error
        if request.method not in ["GET", "POST"]:
            return error_handler.handle(MAGIS_error.HTTP_UNKNOWN_REQUEST_METHOD, None)

        # Extract the requested api-tag (GIS service)
        apiTag_str = str(apiTag).lower()

        # Try to retrieve the correct MAGIS service
        service = apitag2service(apiTag_str, config.SERVICES_DICT_INV)

        # If there is no MAGIS service that goes by that name
        if service is None:
            # Google the inserted string for the user
            return redirect("http://lmgtfy.com/?q=" + apiTag_str, code=302)
        else:
            # Initialize a requestHandler object that handles the incoming request
            req_hdl = RequestHandler(config)

        return req_hdl.handle(request, service)


    # Route documentation
    @app.route('/<apiTag>/doc', methods=['GET', 'POST'])
    def doc(apiTag):

        apiTag_str = str(apiTag).lower()

        service = apitag2service(apiTag_str, dict=config.SERVICES_DICT_INV)

        if service is not None:
            return redirect(config.DOC_REROUTE_DICT[service], code=302)
        else:
            return redirect("http://lmgtfy.com/?q="+apiTag, code=302)

    return app


# Execute this when the MAGIS.py-script is run from a terminal
if __name__ == '__main__':

    cfgReader = MAGISConfigReader()
    config, valid = cfgReader.read(os.path.abspath("./Config/user/MAGIS_user_config.conf"),
                                   config_template_path=os.path.abspath("./Config/MAGIS_config_template.conf"))

    # Startup flask server
    # app = create_app()
    # app.run(debug=True, host=config.MAGIS_HOST,
    #         port=config.MAGIS_PORT)  # Flask development server -> Only for testing purposes

    # Start gunicorn WSGI server
    command = "{gunicorn} -w 2 --reload -b {host}:{port} 'MAGIS:create_app()'".format(gunicorn = config.GUNICORN_PATH, host=config.MAGIS_HOST, port=config.MAGIS_PORT)
    os.system(command)

