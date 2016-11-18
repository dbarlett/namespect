#!/bin/bash
# Download and preprocess NPI file.

mkdir -p npi
cd npi
wget --no-clobber http://download.cms.gov/nppes/NPPES_Data_Dissemination_November_2016.zip
unzip -u NPPES_Data_Dissemination_November_2016.zip
tail --lines=+2 --quiet npidata_20050523-20161113.csv | cut --delimiter "," --fields=6,7,42
