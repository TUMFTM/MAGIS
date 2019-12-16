# MAGIS

Check out our MAGIS-Paper which has been presented at ITSC2019: https://ieeexplore.ieee.org/abstract/document/8917054

## 1. Disclaimer

### 1.1 Sub-GIS

This project makes use of other open source projects, namely OSRM (https://github.com/Project-OSRM/osrm-backend) and
Nominatim (https://github.com/openstreetmap/Nominatim). During MAGIS installation (see section 3.), these projects will 
automatically be downloaded and built from their respective github repositories. 
The MAGIS-Team takes no responsibility for any third party code. Please make sure to respect the licenses under which 
the aforementioned projects are published (https://github.com/Project-OSRM/osrm-backend/blob/master/LICENSE.TXT and 
https://github.com/openstreetmap/Nominatim/blob/master/COPYING).

If you wish to install the needed sub-GIS yourself, please follow the installation instructions under section 4. of this file.   

### 1.2 Deployment Environment

Although the installation and run process of MAGIS has been carefully reviewed, it is only safe to run MAGIS on a dedicated server that you can
easily reset. Never run MAGIS on a system that you can't reset completely in case of doubt.
You are strongly advised to at least install the software on a virtual machine that you can easily manage in case anything goes wrong. 
Be aware that all MAGIS processes require sudo rights.
 
This is research software, not a bulletproof professional business application. You have been warned! 

## 2. Requirements

A Linux system environment is needed in order to deploy MAGIS. The MAGIS reference application was implemented and tested using Debian 9.
We advise you to start with a fresh system without any additional software or user settings in place. The MAGIS 
installation and startup processes require you to be a sudo user.  

For installation and execution of MAGIS you will need a python interpreter. MAGIS was tested using Python 3.5 and 3.6. It is assumed
that your python interpreter can be run using the "python3"-command from a shell. It is furthermore assumed that you have a corresponding
pip installation in place. MAGIS will try to execute pip by calling "pip3" from a shell.

Hardware requirements are heavily dependent on the map data to be used for the setup of MAGIS. They range from only a 
few GB of RAM and disk space to approximately 64 GB of RAM and two TB of disk space for a full planet installation. 

Before installing MAGIS, you have to clone this repository and download an osm.pbf data file that contains the map data of your target region.
You may obtain osm data from geofabrik. You are strongly advised to test MAGIS with a very small map before switching to larger maps. 

## 3. MAGIS Installation including automatic Sub-GIS installation 

This form of installation will serve most users well and is the easiest way of setting up your MAGIS system.

In order to successfully install MAGIS you will need to clone this repository to your Debian 9 system and to save an osm.pbf to the filesystem.
Please make sure to test MAGIS installation and execution with a very small map before switching to larger maps!

Once you have met these requirements, edit the MAGIS configuration file according to your needs. For a full installation of MAGIS including installation
of OSRM and Nominatim, make sure to set the `ONLY_GENERATE_STARTUP_SCRIPT` option to `False`.
After modifying the configuration file you can install MAGIS by running the following command:

`sudo python3 MAGIS_installation.py`

MAGIS will now install and setup all dependencies, including the (Sub-)GIS OSRM and Nominatim.

## 4. Pure MAGIS Installation

This form of installation is suited for experienced users or people who already have Nominatim or OSRM running on their systems.

In order to successfully install MAGIS without any Sub-GIS you will need to clone this repository to your Debian 9 system.

Once you have met the requirements, edit the MAGIS configuration file according to your needs. For a pure installation of MAGIS without installation
of OSRM and Nominatim, make sure to set the `ONLY_GENERATE_STARTUP_SCRIPT` option to `True`.
After modifying the configuration file you can install MAGIS by running the following command:

`sudo python3 MAGIS_installation.py`

MAGIS will now be installed and set up.

In case you choose this option, please make sure to have all necessary MAGIS dependencies installed before you try to execute MAGIS. You will need to have 
the following software in place (sections 4.x):

### 4.1 Nominatim

Nominatim has to be accessible from your MAGIS server. Please provide the
necessary host ip, port number and database user information via Config/MAGIS_config.py.

### 4.2 OSRM

Nominatim has to be accessible from your MAGIS server. Please provide the
necessary host ip, port number and database user information via Config/MAGIS_config.py.

### 4.3 OSM PostgreSQL-DB 
 
For the osmexplorer service, you will need a running PostgreSQL instance
with an OSM database of your target region imported using osmosis.
Please provide the data necessary to access your database via via Config/MAGIS_config.py.

### 5. Run MAGIS

During MAGIS installation, a custom startup script for MAGIS is generated. To run this script and start up MAGIS, make the script executable and execute if from shell:

`sudo chmod a+x MAGIS_custom_startup_script.sh`

`sudo ./MAGIS_custom_startup_script.sh`

This will start MAGIS in three different tmux sessions that you can attach to, in order to monitor MAGIS execution: 

1.  MAGIS `sudo tmux a -t magis` -> MAGIS main service
2.  OSRM `sudo tmux a -t osrm` -> OSRM Sub-GIS
3.  htop `sudo tmux a -t htop` -> Resource monitoring

### 6. Documentation

The documentation will be uploaded to this repository shortly. Until then, see the following examples - which work with a germany-latest.osm.pbf data base - for reference:

* http://<your_magis_server>/geocode?q=Marienplatz&countrycodes=de&limit=5
* http://<your_magis_server>/route?coordinates=[11.671222, 48.264805, 11.624672, 48.247914, 11.584750, 48.188845]
* http://<your_magis_server>/match?coordinates=[11.673744, 48.263214, 11.673212, 48.263485, 11.672665, 48.263449, 11.671978, 48.263678, 11.671066, 48.26377, 11.67085, 48.263685, 11.670884, 48.263378, 11.670423, 48.263049]&time=[2019-01-24 13:01:01,2019-01-24 13:01:02,2019-01-24 13:01:04,2019-01-24 13:01:09,2019-01-24 13:01:10,2019-01-24 13:01:11,2019-01-24 13:01:14,2019-01-24 13:01:15]
* http://<your_magis_server>/reverse?coordinates=[11.62467, 48.2188]
* http://<your_magis_server>/nearest?coordinates=[11.6621, 48.2681]
* http://<your_magis_server>/osmexp?func=wayid2nodes&id=26778733
* http://<your_magis_server>/osmexp?func=wayid2geominfo&id=26778733
* http://<your_magis_server>/osmexp?func=nodeid2geominfo&id=3325534192
