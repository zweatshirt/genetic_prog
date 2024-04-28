#!/usr/bin/bash

# Author: Zachery Linscott

bf="beds"

# Prompt the user to enter the path of the text file containing links
echo "Enter the path of the text file containing bed narrowPeak links:"
read -r file_path
# Check if the file exists
echo "Checking if the text file of links exists..."
if [ ! -f "$file_path" ]; then
    echo "File not found: $file_path"
    exit 1
fi

mkdir $bf

# Read links from the file into an array
echo "Reading le files that were given"
mapfile -t links < "$file_path"

echo "Downloading le files"
# Loop through each link
for link in "${links[@]}"; do
    # Run wget and save output to a file
    wget "$link" -O "${link##*/}"
    mv "${link##*/}" $bf
done


#unzip the bed narrowPeak files
echo "Unzipping le files"
for file in $bf/*; do
    gunzip "$file"
done
