#!/usr/bin/env python
""" This script installs MAGIS on your system
"""

# Imports: 
import os
from Config import MAGIS_config as cfg
import ntpath

__author__ = "Lennart Adenaw"
__copyright__ = "Copyright 2019, Chair of Automotive Technology TU Munich"
__credits__ = ["Lennart Adenaw", "Julian Kreibich", "Michael Wittmann", "Markus Lienkamp"]
__license__ = "GNU GPLv3"
__version__ = "0.0.1"
__maintainer__ = "Lennart Adenaw"
__email__ = "lennart.adenaw@tum.de"
__status__ = "alpha"

# Check if provided data path exists
if not os.path.exists(cfg.OSM_DATA_PATH):
    raise Exception("The provided OSM Data path does not exist on the file system. Please make sure you provide a valid path.")
else:
    osm_data_file_name = ntpath.basename(cfg.OSM_DATA_PATH).split(".")[0]

# MAGIS installation path
magis_installation_base_path = os.path.abspath("")

# Template and script paths
apache_config_template_path = os.path.abspath("./Deployment/ApacheConfigs/apache2_template.conf")
apache_virtual_host_template_path = os.path.abspath("./Deployment/ApacheConfigs/000-default_template.conf")
apache_ports_template_path = os.path.abspath("./Deployment/ApacheConfigs/ports_template.conf")
nominatim_local_template_path = os.path.abspath("./Deployment/NominatimSettings/local_template.php")
magis_installation_template_path = os.path.abspath("./Deployment/Bash/MAGIS_installation_template.sh")
magis_startup_template_path = os.path.abspath("./Deployment/Bash/MAGIS_startup_template.sh")

# Path for custom installation and startup scripts
magis_installation_path = magis_installation_base_path +"/MAGIS_custom_installation_script.sh"
custom_apache_config_path = magis_installation_base_path + "/MAGIS_custom_apache_config.config"
custom_apache_virtual_host_path = magis_installation_base_path + "/MAGIS_custom_apache_virtual_host.config"
custom_apache_ports_path = magis_installation_base_path + "/MAGIS_custom_apache_ports.config"
custom_nominatim_local_path = magis_installation_base_path + "/MAGIS_custom_nominatim_local.php"
custom_magis_startup_path = magis_installation_base_path + "/MAGIS_custom_startup_script.sh"

# Retrieve MAGIS startup template
with open(magis_startup_template_path, 'r') as magis_startup_template_file:
    magis_startup_template = magis_startup_template_file.read()

# Fill MAGIS startup template
magis_startup_template = magis_startup_template.format(SUB_GIS_INSTALLATION_BASE_PATH=cfg.SUB_GIS_INSTALLATION_BASE_PATH, OSM_DATA_DIR=ntpath.dirname(cfg.OSM_DATA_PATH), OSM_DATA_FILE_NAME=osm_data_file_name, MAGIS_INSTALLATION_BASE_PATH=magis_installation_base_path)

# Write MAGIS startup script
with open(custom_magis_startup_path, 'w') as magis_custom_startup_file:
    magis_custom_startup_file.write(magis_startup_template)

if not cfg.ONLY_GENERATE_STARTUP_SCRIPT:
    # Retrieve necessary apache templates
    with open(apache_config_template_path,'r') as apache_config_template_file,\
        open(apache_virtual_host_template_path, 'r') as apache_virtual_host_template_file,\
        open(apache_ports_template_path,'r') as apache_ports_template_file:

        apache_config_template = apache_config_template_file.read()
        apache_virtual_host_template = apache_virtual_host_template_file.read()
        apache_ports_template = apache_ports_template_file.read()

    # Retrieve necessary Nominatim templates
    with open(nominatim_local_template_path, 'r') as nominatim_local_template_file:
        nominatim_local_tempate = nominatim_local_template_file.read()

    # Retrieve MAGIS installation bash script template
    with open(magis_installation_template_path, 'r') as magis_installation_template_file:
        magis_installation_template = magis_installation_template_file.read()

    # Fill Apache templates
    apache_config_template = apache_config_template.format(SUB_GIS_INSTALLATION_BASE_PATH=cfg.SUB_GIS_INSTALLATION_BASE_PATH)

    apache_virtual_host_template = apache_virtual_host_template.format(SUB_GIS_INSTALLATION_BASE_PATH=cfg.SUB_GIS_INSTALLATION_BASE_PATH,
                                                                       NOMINATIM_PORT=cfg.NOMINATIM_PORT)

    apache_ports_template = apache_ports_template.format(NOMINATIM_PORT=cfg.NOMINATIM_PORT)

    # Fill Nominatim template
    nominatim_path = cfg.SUB_GIS_INSTALLATION_BASE_PATH + "/Nominatim"
    nominatim_local_tempate = nominatim_local_tempate.format(NOMINATIM_PATH=nominatim_path,
                                                             NOMINATIM_DB_USER=cfg.NOMINATIM_DB_USER,
                                                             NOMINATIM_DB_USER_PASSWORD=cfg.NOMINATIM_DB_USER_PASSWORD,
                                                             NOMINATIM_PSQL_PORT=cfg.NOMINATIM_PSQL_PORT,
                                                             NOMINATIM_DB_NAME="nominatim",
                                                             NOMINATIM_HOST=cfg.NOMINATIM_HOST)

    # Fill MAGIS installation template
    magis_installation_template = magis_installation_template.format(OSM_DATA_PATH=cfg.OSM_DATA_PATH,
                                                                     OSM_DATA_FILE_NAME = osm_data_file_name,
                                                                     SUB_GIS_INSTALLATION_BASE_PATH=cfg.SUB_GIS_INSTALLATION_BASE_PATH,
                                                                     APACHE_CONFIG_PATH=custom_apache_config_path,
                                                                     APACHE_VIRTUAL_HOST_PATH=custom_apache_virtual_host_path,
                                                                     APACHE_PORTS_PATH=custom_apache_ports_path,
                                                                     NOMINATIM_LOCAL_PATH=custom_nominatim_local_path,
                                                                     NOMINATIM_DB_USER=cfg.NOMINATIM_DB_USER,
                                                                     NOMINATIM_DB_USER_PASSWORD = cfg.NOMINATIM_DB_USER_PASSWORD,
                                                                     OSM_EXPLORER_DB_HOST=cfg.OSM_EXPLORER_DB_HOST,
                                                                     OSM_EXPLORER_DB_NAME=cfg.OSM_EXPLORER_DB_NAME,
                                                                     OSM_EXPLORER_DB_USER=cfg.OSM_EXPLORER_DB_USER,
                                                                     OSM_EXPLORER_DB_PORT=cfg.OSM_EXPLORER_DB_PORT,
                                                                     OSM_EXPLORER_DB_USER_PASSWORD=cfg.OSM_EXPLORER_DB_USER_PASSWORD)

    # Write files necessary for installation
    with open(custom_apache_config_path, 'w') as custom_apache_config_file, \
            open(custom_apache_virtual_host_path, 'w') as custom_apache_virtual_host_file, \
            open(custom_apache_ports_path, 'w') as custom_apache_ports_file, \
            open(custom_nominatim_local_path, 'w') as custom_nominatim_local_file, \
            open(magis_installation_path, 'w') as magis_installation_file:
        custom_apache_config_file.write(apache_config_template)
        custom_apache_virtual_host_file.write(apache_virtual_host_template)
        custom_apache_ports_file.write(apache_ports_template)
        custom_nominatim_local_file.write(nominatim_local_tempate)
        magis_installation_file.write(magis_installation_template)

    # Execute installation script
    os.system("sudo chmod a+x /{MAGIS_INSTALLATION_PATH}".format(MAGIS_INSTALLATION_PATH=magis_installation_path))
    os.system("sudo {MAGIS_INSTALLATION_PATH}".format(MAGIS_INSTALLATION_PATH=magis_installation_path))