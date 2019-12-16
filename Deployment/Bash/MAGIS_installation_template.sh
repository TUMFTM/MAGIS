#!/bin/bash

# Clear the screen
clear

echo '++++ INSTALLING MAGIS ++++'

echo '++++ CREATING NECESSARY DIRECTORIES IF NON-EXISTENT ++++'

mkdir -p {SUB_GIS_INSTALLATION_BASE_PATH}

echo '++++ INSTALLING SYSTEM PACKAGE DEPENDENCIES ++++'

sudo apt-get install -y make cmake g++ libboost-dev libboost-system-dev \
 libboost-filesystem-dev libexpat1-dev zlib1g-dev libboost-thread-dev libboost-regex-dev \
 libbz2-dev libpq-dev libproj-dev lua5.2 liblua5.2-dev \
 libzip-dev libgomp1 liblua5.1-0-dev libgdal-dev libstxxl-dev libsparsehash-dev \
 pkg-config libboost-program-options-dev libboost-iostreams-dev libboost-test-dev \
 libtbb-dev libexpat1-dev \
 postgresql-server-dev-all libxml2-dev postgresql-9.6-postgis-2.3 \
 postgresql-9.6-postgis-scripts \
 apache2 php php-pgsql libapache2-mod-php php-intl wget git curl tmux htop\
 python3-pip unzip openjdk-8-jre\

echo '++++ INSTALLING NOMINATIM ++++'

echo '* NOMINATIM Part A * Download Nominatim'

cd {SUB_GIS_INSTALLATION_BASE_PATH}
git clone --recursive https://github.com/openstreetmap/Nominatim

echo '* NOMINATIM Part B * Create additional directories'

cd {SUB_GIS_INSTALLATION_BASE_PATH}/Nominatim
mkdir build
cd build

echo '* NOMINATIM Part C * Download Country Grid'

cd {SUB_GIS_INSTALLATION_BASE_PATH}/Nominatim/data
wget -O {SUB_GIS_INSTALLATION_BASE_PATH}/Nominatim/data/country_osm_grid.sql.gz https://www.nominatim.org/data/country_grid.sql.gz

echo '* NOMINATIM Part D * Build Nominatim'
cd {SUB_GIS_INSTALLATION_BASE_PATH}/Nominatim/build
cmake ..
make

echo '* NOMINATIM Part E * Setup Nominatim'

sudo mv {NOMINATIM_LOCAL_PATH}  {SUB_GIS_INSTALLATION_BASE_PATH}/Nominatim/settings/local.php

# Create Nominatim Database user if it doesnt exist
sudo -u postgres psql -c "DO \$do\$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '{NOMINATIM_DB_USER}') THEN CREATE ROLE {NOMINATIM_DB_USER} WITH LOGIN PASSWORD '{NOMINATIM_DB_USER_PASSWORD}' CREATEDB;  END IF; END \$do\$;"

# Create Nominatim web-user
sudo -u postgres createuser www-data

cd {SUB_GIS_INSTALLATION_BASE_PATH}/Nominatim/build/utils/
sudo -u postgres ./setup.php --osm-file {OSM_DATA_PATH} --all

echo '* NOMINATIM Part F * Configure Apache for Nominatim'
# Copy correct configuration files to the apache2 server

# Create config backups
sudo mv /etc/apache2/apache2.conf /etc/apache2/apache2_nominatim_installation_backup.conf
sudo mv /etc/apache2/sites-enabled/000-default.conf /etc/apache2/sites-enabled/000-default_nominatim_installation_backup.conf
sudo mv /etc/apache2/ports.conf /etc/apache2/ports_backup.conf

# Point Apache to Nominatim
sudo mv {APACHE_VIRTUAL_HOST_PATH} /etc/apache2/sites-enabled/000-default.conf
sudo mv {APACHE_CONFIG_PATH} /etc/apache2/apache2.conf
sudo mv {APACHE_PORTS_PATH} /etc/apache2/ports.conf
echo 'Restarting Apache2'
sudo service apache2 restart

echo '++++ INSTALLING OSRM ++++'

echo '* OSRM Part A * Creating Directories'

mkdir -p {SUB_GIS_INSTALLATION_BASE_PATH}/osrm
cd {SUB_GIS_INSTALLATION_BASE_PATH}/osrm


echo '* OSRM Part B * Downloading OSRM'

wget https://github.com/Project-OSRM/osrm-backend/archive/v5.20.0.tar.gz
tar -xzf v5.20.0.tar.gz

echo '* OSRM Part C * Building OSRM'

cd {SUB_GIS_INSTALLATION_BASE_PATH}/osrm/osrm-backend-5.20.0/
mkdir -p build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
cmake --build .
sudo cmake --build . --target install

echo '* OSRM Part D * Create routable graph'

GRAPH_DIR=$(dirname "{OSM_DATA_PATH}")
{SUB_GIS_INSTALLATION_BASE_PATH}/osrm/osrm-backend-5.20.0/build/osrm-extract {OSM_DATA_PATH} -p {SUB_GIS_INSTALLATION_BASE_PATH}/osrm/osrm-backend-5.20.0/profiles/car.lua
{SUB_GIS_INSTALLATION_BASE_PATH}/osrm/osrm-backend-5.20.0/build/osrm-contract $GRAPH_DIR/{OSM_DATA_FILE_NAME}.osrm

echo '++++ INSTALLING OSMEXPLORER ++++'

echo '* OSMEXPLORER Part A * Installing Osmosis'

mkdir -p {SUB_GIS_INSTALLATION_BASE_PATH}/osmosis
cd {SUB_GIS_INSTALLATION_BASE_PATH}/osmosis
wget https://bretth.dev.openstreetmap.org/osmosis-build/osmosis-latest.zip
unzip osmosis-latest
chmod a+x {SUB_GIS_INSTALLATION_BASE_PATH}/osmosis/bin/osmosis

echo '* OSMEXPLORER Part B * Creating OSM DB'

# Create OSM-explorer Database user if it doesnt exist
sudo -u postgres psql -c "DO \$do\$ BEGIN IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '{OSM_EXPLORER_DB_USER}') THEN CREATE ROLE {OSM_EXPLORER_DB_USER} WITH LOGIN CREATEDB;  END IF; END \$do\$;"
sudo -u postgres psql -c "ALTER USER {OSM_EXPLORER_DB_USER} WITH PASSWORD '{OSM_EXPLORER_DB_USER_PASSWORD}';"
sudo -u postgres psql -c "CREATE DATABASE {OSM_EXPLORER_DB_NAME} WITH owner={OSM_EXPLORER_DB_USER}"
sudo -u postgres psql {OSM_EXPLORER_DB_NAME} -c "CREATE EXTENSION postgis;"
sudo -u postgres psql {OSM_EXPLORER_DB_NAME} -c "CREATE EXTENSION hstore;"
sudo -u postgres psql {OSM_EXPLORER_DB_NAME} -f {SUB_GIS_INSTALLATION_BASE_PATH}/osmosis/script/pgsnapshot_schema_0.6.sql


# Give necessary rights to osm_explorer database user
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE {OSM_EXPLORER_DB_NAME} TO {OSM_EXPLORER_DB_USER};"
sudo -u postgres psql {OSM_EXPLORER_DB_NAME} -c "ALTER TABLE schema_info OWNER TO {OSM_EXPLORER_DB_USER}"
sudo -u postgres psql {OSM_EXPLORER_DB_NAME} -c "ALTER TABLE nodes OWNER TO {OSM_EXPLORER_DB_USER}"
sudo -u postgres psql {OSM_EXPLORER_DB_NAME} -c "ALTER TABLE relation_members OWNER TO {OSM_EXPLORER_DB_USER}"
sudo -u postgres psql {OSM_EXPLORER_DB_NAME} -c "ALTER TABLE relations OWNER TO {OSM_EXPLORER_DB_USER}"
sudo -u postgres psql {OSM_EXPLORER_DB_NAME} -c "ALTER TABLE spatial_ref_sys OWNER TO {OSM_EXPLORER_DB_USER}"
sudo -u postgres psql {OSM_EXPLORER_DB_NAME} -c "ALTER TABLE users OWNER TO {OSM_EXPLORER_DB_USER}"
sudo -u postgres psql {OSM_EXPLORER_DB_NAME} -c "ALTER TABLE way_nodes OWNER TO {OSM_EXPLORER_DB_USER}"
sudo -u postgres psql {OSM_EXPLORER_DB_NAME} -c "ALTER TABLE ways OWNER TO {OSM_EXPLORER_DB_USER}"

echo '* OSMEXPLORER Part C * Populating OSM DB ++++'

cd {SUB_GIS_INSTALLATION_BASE_PATH}/osmosis/bin
sudo ./osmosis --read-pbf {OSM_DATA_PATH} --log-progress --write-pgsql host={OSM_EXPLORER_DB_HOST}:{OSM_EXPLORER_DB_PORT} database={OSM_EXPLORER_DB_NAME} user={OSM_EXPLORER_DB_USER} password={OSM_EXPLORER_DB_USER_PASSWORD}

echo '++++ INSTALLING MAGIS PYTHON DEPENDENCIES ++++'

sudo pip3 install flask
sudo pip3 install psycopg2
sudo pip3 install geopandas
sudo pip3 install geojson
sudo pip3 install sshtunnel

# Go home
cd ~