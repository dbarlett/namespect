#!/bin/bash
# Download and preprocess state voter files.

mkdir -p states
cd states

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
  wget --no-clobber --directory-prefix=$ST http://connvoters.com/downloads/20160209/votelct$i.zip
  unzip -u -d $ST $ST/votelct$i.zip
done
# Last, First, DOB, Gender
cut --delimiter "," -f 3,4,38,42 $ST/SSP/ELCT/VOTER/EXT* | tr --delete " " > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"

ST=DE
STATE=Delaware
echo "Downloading $STATE data to $ST"
wget --no-clobber --directory-prefix=$ST http://delawarevoters.info/download/20150521/ActiveReg.csv
# Last, First, YOB
tail --lines=+2 $ST/ActiveReg.csv | cut --delimiter "," -f 2,3,6 > $ST/$ST.csv
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
wget --no-clobber --directory-prefix=$ST http://michiganvoters.info/download/20160901/FOIA_VOTERS.zip
unzip -u -d $ST $ST/FOIA_VOTERS.zip
# Last, First, Birth Year, Gender
cut --output-delimiter="," --characters=1-35,36-55,79-82,83 $ST/entire_state_v.lst | tr --delete " " > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"

ST=NC
STATE="North Carolina"
echo "Downloading $STATE data to $ST"
wget --no-clobber --directory-prefix=$ST https://s3.amazonaws.com/dl.ncsbe.gov/data/ncvoter_Statewide.zip
unzip -u -d $ST $ST/ncvoter_Statewide.zip
# Last, First, Gender, Age
tail --lines=+2 $ST/ncvoter_Statewide.txt | cut --output-delimiter="," --fields=10,11,29,30 > $ST/$ST.csv
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
wget --no-clobber --directory-prefix=$ST http://rivoters.com/download/2015-01.txt
# Last, First, DOB, Gender
tail --lines=+3 $ST/2015-01.txt | cut --delimiter="|" --output-delimiter="," --fields=3,4,35,38 > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"

ST=VT
STATE=Vermont
# Last, First, YOB
tail --lines=+3 $ST/*.txt | cut --delimiter="|" --output-delimiter="," --fields=2,3,13 > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"

ST=WA
STATE=Washington
echo "Downloading $STATE data to $ST"
wget --no-clobber --directory-prefix=$ST http://www.sos.wa.gov/elections/vrdb/download/vrdb-current.zip
unzip -u -d $ST $ST/vrdb-current.zip
# First, Last, DOB, Gender
tail --lines=+2 $ST/20161031_VRDB_Extract.txt | cut --output-delimiter="," --only-delimited --fields=4,6,8,9 > $ST/$ST.csv
echo "Wrote $STATE data to $ST/$ST.csv"