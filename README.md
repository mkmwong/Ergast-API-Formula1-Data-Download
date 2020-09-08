# Ergast API Formula1 Data Download
This is a short script for downloading all available formula1 data, excluding laptimes, from [Ergast API](http://ergast.com/mrd/) into csv files.

To use this , first clone this repository.
```
git clone https://github.com/mkmwong/Ergast-API-Formula1-Data-Download
```
Then, run the script by calling 
```
cd Ergast-API-Formula1-Data-Download
./downloadresult.sh full_path_target_dir
```
full_path_target_dir would be the location where you would like to save your target files, for example `~/Desktop/tmp` .

Alternatively, the data is available in data/ in this repository. It includes all the data including and up to 2020 Hungarian GP.
