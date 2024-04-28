#!/usr/bin/bash

# Author: Zachery Linscott

echo "run this by using source NOT ./script1_installs.sh"

#read -p "Please provide the server host (e.g. zlinsco@pc533.emulab.net): " user

# Update, htop, and screen install
echo "Updating... Additionally, installing htop and screen"
sudo apt-get update
sudo install htop
sudo install screen


# # Jupyter Notebook install
# echo "Time to install jupyter notebook."
# conda install -c conda-forge notebook
# conda install -c conda-forge nb_conda_kernels
# conda install nb_conda

echo "Installing gunzip to unzip the bed file..."
sudo apt-get install gzip
echo "Installing bedtools as well"
sudo apt-get install bedtools
echo "Runing sudo apt-get update to ensure bedtools and gunzip can be installed correctly"
sudo apt-get update