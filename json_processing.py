import json
import csv
import sys
import os
import pandas as pd
import numpy as np

def processing_json(input_f, type_f, out_f):
  with open(input_f) as json_file:
    #print('Reading json...')
    dat = json.load(json_file)
    if type_f == 'seasons':
      sub_dat = dat['MRData']['SeasonTable']['Seasons']
    elif type_f == 'drivers':
      sub_dat = dat['MRData']['DriverTable']['Drivers']
    elif type_f == 'constructors':
      sub_dat = dat['MRData']['ConstructorTable']['Constructors']
    elif type_f == 'circuits':
      sub_dat = dat['MRData']['CircuitTable']['Circuits']
      sub_dat = pd.json_normalize(sub_dat)
    else:
      sub_dat = dat['MRData']['StatusTable']['Status']
    df = pd.DataFrame.from_dict(sub_dat)
    df.to_csv(out_f, index=False)

def processing_folder(input_f, type_f, out_f):
  count = 0
  if type_f == 'schedule':
    for f in os.listdir(input_f):
      full_path_f = input_f + '/' + f
      with open(full_path_f) as json_file:
        dat = json.load(json_file)
        if count == 0:
          summ = pd.json_normalize(dat['MRData']['RaceTable']['Races'])
        elif count > 0:
          df = pd.json_normalize(dat['MRData']['RaceTable']['Races'])
          summ = summ.append(df)
        count += 1
    summ = summ.drop(['Circuit.url','Circuit.circuitName','Circuit.Location.lat','Circuit.Location.long','Circuit.Location.locality','Circuit.Location.country'], axis=1)
    summ = summ.rename(columns={"Circuit.circuitId":"circuitId"})
  else:
    if type_f == 'qualifying':
      tmp = ['RaceTable','Races','QualifyingResults']
    elif type_f == 'results':
      tmp = ['RaceTable','Races','Results']
    elif type_f == 'constructorStandings':
      tmp = ['StandingsTable','StandingsLists', 'ConstructorStandings']
    elif type_f == 'driverStandings':
      tmp = ['StandingsTable','StandingsLists', 'DriverStandings']
    else:
      tmp = ['RaceTable','Races','PitStops']
    for f in os.listdir(input_f):
      full_path_f = input_f + '/' + f
      with open(full_path_f) as json_file:
        dat = json.load(json_file)
        if count == 0:
          summ = pd.json_normalize(dat['MRData'][tmp[0]][tmp[1]],tmp[2],['season','round'])
        elif count > 0:
          df = pd.json_normalize(dat['MRData'][tmp[0]][tmp[1]],tmp[2],['season','round'])
          summ = summ.append(df)
        count += 1
    if type_f == 'qualifying' or type_f == 'results':
      summ = summ.drop(['Driver.permanentNumber','Driver.code','Driver.url','Driver.givenName','Driver.familyName','Driver.dateOfBirth','Driver.nationality','Constructor.url','Constructor.name','Constructor.nationality'], axis=1)
      summ = summ.rename(columns={"Driver.driverId":"driverId", "Constructor.constructorId":"constructorId"})
    elif type_f == 'constructorStandings': 
      summ = summ.drop(['Constructor.url','Constructor.name','Constructor.nationality'], axis=1)
      summ = summ.rename(columns={"Constructor.constructorId":"constructorId"})
    elif type_f == 'driverStandings':
     summ = summ.drop(['Constructors','Driver.url','Driver.givenName','Driver.familyName','Driver.dateOfBirth','Driver.nationality','Driver.code','Driver.permanentNumber'], axis=1)
  summ.to_csv(out_f, index=False)

def call_processing(input_f):
  input_f = sys.argv[1]
  type_f = input_f.split('.')[0]
  out_f = type_f+'.csv'
  print('Processing ' + type_f + 'file ...')
  if len(input_f.split('.')) == 2:
    processing_json(input_f, type_f, out_f)
  else:
    processing_folder(input_f, type_f, out_f)

call_processing(sys.argv[1])

