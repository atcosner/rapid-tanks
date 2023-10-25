import csv
from pathlib import Path

DIRECTORY = Path(r'D:\Documents\PycharmProjects\rapid-tanks\scratch')

csv_lines = [
    [
        'name',
        'cas_number',
        'molecular_weight',
        'liquid_density',
        'true_vapor_pressure',
        'antoine_a',
        'antoine_b',
        'antoine_c',
        'antoine_min_temp',
        'antoine_max_temp',
        'normal_boiling_point',
    ],
]

# Get all files
files = sorted(list(DIRECTORY.glob('*.txt')))
for file in files:
    with file.open('rt') as file_obj:
        lines = [line.strip() for line in file_obj.readlines()]

        # Each chemical should have 11 lines so the total file should be a multiple of 11
        if remainder := len(lines) % 11:
            raise RuntimeError(f'File length was not a multiple of 11! Rem: {remainder}')

        # Break the line into chemical chunks
        for line_start_idx in range(0, len(lines), 11):
            chem_lines = lines[line_start_idx:line_start_idx + 11]
            print(chem_lines)
            csv_lines.append(chem_lines)

# Write out the CSV
with (DIRECTORY / 'table_7_1_3.csv').open('w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(csv_lines)
