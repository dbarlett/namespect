#!/bin/bash
# Download and preprocess state voter files.

mkdir -p states
cd states

ST=AR
STATE=Arkansas
wget --no-clobber --directory-prefix=$ST https://arkvoters.com/download/20200218/VR_VH.zip
unzip -u -d $ST $ST/VR_VH.zip
# DOB, Last, First
tail --quiet --lines=+2 --quiet $ST/VR_VH.csv | cut --delimiter="," -f 6,9,10 > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"
ST=CO
STATE=Colorado
echo "Downloading $STATE data to $ST"
for i in {1..14};
do
  wget --no-clobber --directory-prefix=$ST http://coloradovoters.info/downloads/20160201/part$i.zip
  unzip -u -d $ST $ST/part$i.zip
done
# Last, First, Birth Year, Gender
tail --lines=+2 --quiet $ST/Registered_Voters_List_\ Part*.txt | cut --delimiter="," -f 4,5,31,32 > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"

ST=CT
STATE=Connecticut
echo "Downloading $STATE data to $ST"
for i in {1..4};
do
  wget --no-clobber --directory-prefix=$ST https://connvoters.com/downloads/20191231/VOTELCT$i.ZIP
  unzip -u -d $ST $ST/VOTELCT$i.ZIP
done
# Last, First, DOB, Gender
cut --delimiter "," -f 3,4,38,42 $ST/SSP/ELCT/VOTER/EXT* | tr --delete " " > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"

ST=DE
STATE=Delaware
echo "Downloading $STATE data to $ST"
wget --no-clobber --directory-prefix=$ST https://delawarevoters.info/download/20150521/ActiveReg.csv
# Last, First, YOB
tail --quiet --lines=+2 $ST/ActiveReg.csv | cut --delimiter "," -f 2,3,6 > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"

ST=FL
STATE=Florida
echo "Downloading $STATE data to $ST"
wget -r --no-clobber --no-parent --no-host-directories --cut-dirs=3 --reject="index.html" --directory-prefix=$ST http://flvoters.com/download/20161031/20161101_VoterDetail/
# Last, First, Gender, DOB
cut --output-delimiter="," --fields=3,5,20,22 $ST/*_20161101.txt > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"

ST=MI
STATE=Michigan
echo "Downloading $STATE data to $ST"
wget --no-clobber --directory-prefix=$ST https://michiganvoters.info/download/20200302/EntireStateVoter.zip
unzip -u -d $ST $ST/EntireStateVoter.zip
# Last, First, YOB, Gender
tail --quiet --lines=+2 $ST/EntireStateVoters.csv | cut --delimiter="," --output-delimiter="," --fields=1,2,5,6 > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"

ST=NC
STATE="North Carolina"
echo "Downloading $STATE data to $ST"
wget --no-clobber --directory-prefix=$ST https://s3.amazonaws.com/dl.ncsbe.gov/data/ncvoter_Statewide.zip
unzip -u -d $ST $ST/ncvoter_Statewide.zip
# Last, First, Gender, Age
tail --lines=+2 $ST/ncvoter_Statewide.txt | cut --output-delimiter="," --fields=10,11,29,30 > $ST/$ST.csv

ST=NV
STATE=Nevada
# Run report manually and download
# First, Last, DOB
cut --delimiter="," --output-delimiter="," --fields=2,3,4 $ST/VoterList*.csv > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"

ST=OH
STATE=Ohio
echo "Downloading $STATE data to $ST"
wget --no-clobber --directory-prefix=$ST ftp://sosftp.sos.state.oh.us/free/Voter/SWVF_1_44.zip
wget --no-clobber --directory-prefix=$ST ftp://sosftp.sos.state.oh.us/free/Voter/SWVF_45_88.zip
unzip -u -d $ST $ST/SWVF_1_44.zip
unzip -u -d $ST $ST/SWVF_45_88.zip
# Last, First, DOB
tail --lines=+2 $ST/*.TXT | cut --delimiter="," --fields=4,5,8 > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"

ST=RI
STATE="Rhode Island"
echo "Downloading $STATE data to $ST"
wget --no-clobber --directory-prefix=$ST https://rivoters.com/download/2017-01.txt
# Last, First, DOB, Gender
tail --quiet --lines=+3 $ST/2017-01.txt | cut --delimiter="|" --output-delimiter="," --fields=3,4,35,38 > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"

ST=VT
STATE=Vermont
# Last, First, YOB
tail --lines=+3 $ST/*.txt | cut --delimiter="|" --output-delimiter="," --fields=2,3,13 > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"

ST=WA
STATE=Washington
# Manual download
unzip -u -d $ST $ST/2913643776.zip
# First, Last, DOB, Gender
tail --quiet --lines=+2 $ST/*_VRDB_Extract_2.txt | cut --delimiter "|" --output-delimiter="," --fields=2,4,6,7 > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"
