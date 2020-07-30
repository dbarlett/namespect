#!/bin/bash
# Download and preprocess NPI file.

mkdir -p npi
cd npi
wget --no-clobber https://download.cms.gov/nppes/NPPES_Data_Dissemination_July_2020.zip
unzip -u NPPES_Data_Dissemination_July_2020.zip
tail --lines=+2 --quiet npidata_pfile_20050523-20200712.csv | cut --delimiter "," --fields=6,7,42 | grep --invert-match '"","",""' > NPI.csv
