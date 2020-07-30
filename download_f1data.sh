target_dir=$1

################### 1. Downloading seasons information ###################
#### Processed to obtain info to download season specific information #### 
echo 'Downloading season specific data...'
wget -q -O seasons.json http://ergast.com/api/f1/seasons.json?limit=80
python3 json_processing.py seasons.json

################## 2. Downloading drivers information ####################
echo 'Downloading driver data...'
wget -q -O drivers.json http://ergast.com/api/f1/drivers.json?limit=900
python3 json_processing.py drivers.json

############### 3. Downloading constructors information ##################
echo 'Downloading constructor data...'
wget -q -O constructors.json http://ergast.com/api/f1/constructors.json?limit=230
python3 json_processing.py constructors.json

################## 4. Downloading circuit information ####################
echo 'Downloading circuit data...'
wget -q -O circuits.json http://ergast.com/api/f1/circuits.json?limit=80
python3 json_processing.py circuits.json

############### 5. Downloading finish status information #################
echo 'Downloading status data...'
wget -q -O status.json http://ergast.com/api/f1/status.json?limit=140
python3 json_processing.py status.json

###################### 6. Downloading race schedule ######################
lst=($(awk 'BEGIN {FS=","}; NR>1 {print $1}' seasons.csv))
#echo $lst
echo 'Downloading race schedule data...'
for i in "${lst[@]}"; do 
  wget -q -O schedule_$i.json http://ergast.com/api/f1/$i.json
done
mkdir schedule
mv schedule*json schedule/
python3 json_processing.py schedule
rm -rf schedule
##################### 7. Downloading the rest ############################
season=($(awk 'BEGIN {FS=","}; NR>1 {print $1}' schedule.csv))
round=($(awk 'BEGIN {FS=","}; NR>1 {print $2}' schedule.csv))
len=${#season[@]}
features=(results
          qualifying
          driverStandings
          constructorStandings
          pitstops)

echo 'Downloading per-round data... might take awhile'
for ((i=0; i<len; i++)); do
  for j in ${features[@]}; do
    wget -q -O $j'_'${season[i]}'_'${round[i]}'.json' 'http://ergast.com/api/f1/'${season[i]}'/'${round[i]}'/'$j'.json'
  done
done

mkdir qualifying
mkdir results
mkdir driverStandings
mkdir constructorStandings
mkdir pitstops

mv qualifying*json qualifying
mv results*json results
mv driverStanding*json driverStandings
mv constructorStanding*json constructorStandings
mv pitstops*json pitstops

python3 json_processing.py qualifying
python3 json_processing.py results
python3 json_processing.py constructorStandings
python3 json_processing.py driverStandings
python3 json_processing.py pitstops

mkdir $target_dir
mv *csv $target_dir

rm -rf qualifying
rm -rf results
rm -rf driverStandings
rm -rf constructorStandings
rm -rf pitstops

rm -rf *.json 














