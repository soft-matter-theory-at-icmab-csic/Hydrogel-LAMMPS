awk -F '\ ' '{print $2}' heparin-bonds.dat | tail -n +2| sort | uniq -c | sort -nr > histogram.dat
awk -F '\ ' '{print $2}' PEG-bonds.dat | tail -n +2| sort | uniq -c | sort -nr > hist-PEG.dat
