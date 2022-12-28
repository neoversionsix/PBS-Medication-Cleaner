import os
import pathlib as pth

# This will get the name of the folder we want
folder_1 = pth.Path('//whoffice/shared/EMR/BAU/Audit Spreadsheets/PBS audits/')
all_folder_names = os.listdir(folder_1)
folder_names = []

for item in all_folder_names:
    try:
        folder_names.append(int(item))
    except ValueError:
        continue

folder_names.sort(reverse=True)

folder = folder_names[0]

