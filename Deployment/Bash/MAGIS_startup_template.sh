#!/bin/bash

echo "This scipt will start up MAGIS on this machine"

# Make sure this script is executed from a super user
if [ "$EUID" -ne 0 ]
  then echo "Error: This script has to be run with root privileges. Please run as root!"
  exit
fi

# Create a tmux session for osrm
sudo tmux new-session -d -s osrm
sudo tmux send-keys -t "osrm:0" "{SUB_GIS_INSTALLATION_BASE_PATH}/osrm/osrm-backend-5.20.0/build/osrm-routed {OSM_DATA_DIR}/{OSM_DATA_FILE_NAME}.osrm --max-matching-size 100000" Enter

# Start up a tmux session for resource monitoring
sudo tmux new-session -d -s htop htop

# Start up a tmux session for the http-Server
sudo tmux new-session -d -s magis
sudo tmux send-keys -t "magis:0" "cd {MAGIS_INSTALLATION_BASE_PATH} && python3 MAGIS.py" Enter

# List all created tmux sessions

echo "The following tmux sessions have been started and MAGIS is running!"

sudo tmux ls


