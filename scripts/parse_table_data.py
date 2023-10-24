from pathlib import Path

DIRECTORY = Path(r'D:\Documents\PycharmProjects\rapid-tanks\scratch')

# Get all files
files = sorted(list(DIRECTORY.glob('*')))
for file in files:
    print(file)

    with file.open('rt') as file_obj:
        lines = [line.strip() for line in file_obj.readlines()]

        # for line_start_idx in range(0, len(lines), 11):
        #     chem_lines = lines[line_start_idx:line_start_idx + 11]
        #     for line in chem_lines:
        #         print(line)
        #     print()

        # Each chemical should have 11 lines
        if remainder := len(lines) % 11:
            raise RuntimeError(f'File length was not a multiple of 11! Rem: {remainder}')
