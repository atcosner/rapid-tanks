import pandas as pd

cities = ['Birmingham, AL', 'Huntsville, AL', 'Mobile, AL']
symbols = ['T~AN', 'T~AX', 'V', 'I', 'P~A']

index = pd.MultiIndex.from_product([cities, symbols], names=['cities', 'symbols'])
print(index)
