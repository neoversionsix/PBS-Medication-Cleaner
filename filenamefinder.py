import os
import pathlib as pth

folder_1 = pth.Path('//whoffice/shared/EMR/BAU/Audit Spreadsheets/PBS audits/')

folders = os.listdir(folder_1)
print(folders)