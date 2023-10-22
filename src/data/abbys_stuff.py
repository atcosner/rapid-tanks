# all meteorological data downloaded from below website to maintain consistency with AP-42
# https://www1.ncdc.noaa.gov/pub/data/nsrdb-solar/summary-stats-2010/dailystats/
import pandas
import pandas as pd
from pathlib import Path

DIRECTORY = Path('C:/Users/Abby/PycharmProjects/rapid-tanks')
data = pd.read_csv(DIRECTORY / 'met/NSRDB_DailyStatistics_19910101_20101231_700260.txt',
                   skiprows=[0, 1], delim_whitespace=True)
data = data.loc[12, ]
print(data)
