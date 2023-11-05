# all meteorological data downloaded from below website to maintain consistency with AP-42
# https://www1.ncdc.noaa.gov/pub/data/nsrdb-solar/summary-stats-2010/dailystats/
import pandas
import pandas as pd
from pathlib import Path

DIRECTORY = Path('C:/Users/Abby/PycharmProjects/rapid-tanks')
name = pd.read_csv(DIRECTORY / 'met/NSRDB_DailyStatistics_19910101_20101231_722900.txt')
data = pd.read_csv(DIRECTORY / 'met/NSRDB_DailyStatistics_19910101_20101231_722900.txt',
                   skiprows=[0, 1], delim_whitespace=True)

data = data.loc[0:12, ['MIN_T', 'MAX_T', 'AVWS', 'AVGLO']]
data.loc[:, 'MIN_T'] = data.loc[:, 'MIN_T'] * 9/5 + 32
data.loc[:, 'MAX_T'] = data.loc[:, 'MAX_T'] * 9/5 + 32
data.loc[:, 'AVWS'] = data.loc[:, 'AVWS'] * 2.237
data.loc[:, 'AVGLO'] = data.loc[:, 'AVGLO'] * 3.41214 / 10.7639

name = name.loc[1, ]
name = pd.Series.to_string(name)
name = name.split()
name = name[:-12]
loc_code = name[0]
lat = ' '.join(name[-4:-2])
long = ' '.join(name[-2:])
state = name[-6]
name = name[1:]
name = name[:-6]
name = ' '.join(name)

print(f'{name}, {state}, {loc_code}, {lat}, {long}')
