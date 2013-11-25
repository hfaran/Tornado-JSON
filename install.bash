#!/bin/bash

LOGDIR="/var/log/touchpoint/"
ORIGUSER="$USER"

# Install any system packages (Ubuntu/Debian only) that are pre-requisites
echo -e "\n\nInstalling required system packages . . ."
sudo apt-get install libffi-dev

# Install all required Python packages
echo -e "\n\nInstalled required Python packages with pip . . ."
sudo pip install -r requirements.txt

# Bootstrap the DB
echo -e "\n\nAbout the boostrap the DB; please enter your MySQL root user password"
mysql -uroot -p < bootstrapdb.sql

# Create log directory and give $USER access to the folder
sudo mkdir -p $LOGDIR
sudo setfacl -m user:$ORIGUSER:rwx $LOGDIR


echo -e "\n\nBootstrapping complete."
