#!/bin/bash
# Download and preprocess state voter files (uses 17.1 GB)

ST=states/CO
echo "Downloading Colorado data to $ST/"
for i in {1..14};
do
  wget --no-clobber --directory-prefix=$ST http://coloradovoters.info/downloads/20151001/Part$i.zip
  unzip -u -d $ST $ST/Part$i.zip
done
# Last, First, Birth Year, Gender
tail --lines=+2 --quiet $ST/Registered_Voters_List_\ Part*.txt | cut --delimiter="," -f 4,5,31,32 > $ST/$ST.csv
echo "Wrote Colorado data to $ST/$ST.csv"

ST=states/CT
echo "Downloading Connecticut data to $ST/"
for i in {1..4};
do
  wget --no-clobber --directory-prefix=$ST  http://connvoters.com/downloads/20141202/VOTELCT$i.ZIP
  unzip -u -d $ST $ST/VOTELCT$i.ZIP
done
# Last, First, DOB, Gender
cut --delimiter "," -f 3,4,38,42 $ST/SSP/ELCT/VOTER/EXT* > $ST/$ST.csv
echo "Wrote Connecticut data to $ST/$ST.csv"

ST=states/FL
echo "Downloading Florida data to $ST/"
wget --no-clobber --directory-prefix=$ST http://flvoters.com/download/20150831/20150831.zip
unzip -u -d $ST $ST/20150831.zip
# Last, First, Gender, DOB
cut --output-delimiter="," --fields=3,5,20,22 $ST/*_20150917.txt > $ST/$ST.csv
echo "Wrote Florida data to $ST/$ST.csv"

ST=states/MI
echo "Downloading Michigan data to $ST/"
wget --no-clobber --directory-prefix=$ST http://web.archive.org/web/20150313234052/http://michiganvoters.info/download/20140901/foia_voters.zip
unzip -u -d $ST $ST/foia_voters.zip
# Last, First, Birth Year, Gender
tail --lines=+2 $ST/foi_bas* | cut --output-delimiter="," --characters=1-35,36-55,79-82,83 | tr --delete " " > $ST/$ST.csv
echo "Wrote Michigan data to $ST/$ST.csv"

ST=states/NC
echo "Downloading North Carolina data to $ST/"
wget --no-clobber --directory-prefix=$ST ftp://alt.ncsbe.gov/data/ncvoter_Statewide.zip
unzip -u -d $ST $ST/ncvoter_Statewide.zip
# Last, First, Gender, Age
tail --lines=+2 $ST/ncvoter_Statewide.txt | cut --output-delimiter="," --fields=10,11,29,30 > $ST/$ST.csv
echo "Wrote North Carolina data to $ST/$ST.csv"

ST=states/RI
echo "Downloading Rhode Island data to $ST/"
wget --no-clobber --directory-prefix=$ST http://rivoters.com/download/2015-01.txt
# Last, First, DOB, Gender
tail --lines=+3 $ST/2015-01.txt | cut --delimiter="|" --output-delimiter="," --fields=3,4,35,38 > $ST/$ST.csv
echo "Wrote Rhode Island data to $ST/$ST.csv"

ST=states/WA
echo "Downloading Washington data to $ST/"
wget --no-clobber --directory-prefix=$ST http://www.sos.wa.gov/elections/vrdb/download/vrdb-current.zip
unzip -u -d $ST $ST/vrdb-current.zip
tail --lines=+2 $ST/201510_VRDB_Extract.txt | cut --output-delimiter="," --only-delimited --fields=4,6,8,9 > $ST/$ST.csv
echo "Wrote Washington data to $ST/$ST.csv"
