# all meteorological data downloaded from below website to maintain consistency with AP-42
# https://www1.ncdc.noaa.gov/pub/data/nsrdb-solar/summary-stats-2010/dailystats/
import pandas as pd
from pathlib import Path
import glob2

us_state_to_abbrev = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
    "District of Columbia": "DC",
    "American Samoa": "AS",
    "Guam": "GU",
    "Northern Mariana Islands": "MP",
    "Puerto Rico": "PR",
    "United States Minor Outlying Islands": "UM",
    "U.S. Virgin Islands": "VI",
}

# invert the dictionary
abbrev_to_us_state = dict(map(reversed, us_state_to_abbrev.items()))

DIRECTORY = Path('C:/Users/acath/PycharmProjects/rapid-tanks')
met_data = (DIRECTORY / 'met')

f = open('C:/Users/acath/PycharmProjects/rapid-tanks/scratch/compiled_met.txt', 'w')
filenames = glob2.glob('C:/Users/acath/PycharmProjects/rapid-tanks/met/*.txt')
i = filenames[1]
for i in filenames:
    name = pd.read_csv(i)
    data = pd.read_csv(i, skiprows=[0, 1], delim_whitespace=True)

    data = data.loc[0:12, ['MIN_T', 'MAX_T', 'AVWS', 'AVGLO']]
    data.loc[:, 'MIN_T'] = data.loc[:, 'MIN_T'] * 9/5 + 32
    data.loc[:, 'MIN_T'] = round(data.loc[:, 'MIN_T'], 1)
    data.loc[:, 'MAX_T'] = data.loc[:, 'MAX_T'] * 9/5 + 32
    data.loc[:, 'MAX_T'] = round(data.loc[:, 'MAX_T'], 1)
    data.loc[:, 'AVWS'] = data.loc[:, 'AVWS'] * 2.237
    data.loc[:, 'AVWS'] = round(data.loc[:, 'AVWS'], 1)
    data.loc[:, 'AVGLO'] = data.loc[:, 'AVGLO'] * 3.41214 / 10.7639
    data.loc[:, 'AVGLO'] = round(data.loc[:, 'AVGLO'], 0)

    name = name.loc[1, ]
    name = pd.Series.to_string(name)
    name = name.split()
    name = name[:-10]
    pressure = round(int(name[-1]) * 0.0145038, 2)
    name = name[:-2]
    loc_code = name[0]
    lat = ' '.join(name[-4:-2])
    long = ' '.join(name[-2:])
    state = abbrev_to_us_state[name[-6]]
    name = name[1:]
    name = name[:-6]
    name = ' '.join(name)

    f.write(f"('{name}', '{state}', '{loc_code}', '{lat}', '{long}', '{pressure}',\n    [\n")

    for index, row in data.iterrows():
        f.write(f"        ('{index+1}', '{row[0]}', '{row[1]}', '{row[2]}', '{row[3]}'),\n")

    f.write('    ],\n),\n')

f.close()
