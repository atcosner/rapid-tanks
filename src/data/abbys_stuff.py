# all meteorological data downloaded from below website to maintain consistency with AP-42
# https://www1.ncdc.noaa.gov/pub/data/nsrdb-solar/summary-stats-2010/dailystats/
import pandas
import pandas as pd
from pathlib import Path

DIRECTORY = Path('C:/Users/Abby/PycharmProjects/rapid-tanks')
name = pd.read_csv(DIRECTORY / 'met/NSRDB_DailyStatistics_19910101_20101231_700260.txt')
data = pd.read_csv(DIRECTORY / 'met/NSRDB_DailyStatistics_19910101_20101231_700260.txt',
                   skiprows=[0, 1], delim_whitespace=True)


data = data.loc[0:12, ['MIN_T', 'MAX_T', 'AVWS', 'AVGLO']]
name = name.loc[1, ]
name = pd.Series.to_string(name)
name = name.split()
name = name[:-12]
loc_code = name[0]
lat = name[-4:-2]
long = name[-2:]
state = name[-6]
name = name[1:]
name = name[:-6]
name = ' '.join(name)

#TODO convert T windspeed and AVGLO (Wh/m2 to Btu/ft2)

print(state)
print(data)
print(name)
