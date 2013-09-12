#!/bin/bash


# Install any system packages (Ubuntu/Debian only) that are pre-requisites
echo -e "\n\nInstalling required system packages . . ."
sudo apt-get install libffi-dev

# Install all required Python packages
echo -e "\n\nInstalled required Python packages with pip . . ."
sudo pip install -r requirements.txt

# Bootstrap the DB
echo -e "\n\nAbout the boostrap the DB; please enter your MySQL root user password"
mysql -uroot -p < bootstrapdb.sql

echo -e "\n\nBootstrapping complete."

