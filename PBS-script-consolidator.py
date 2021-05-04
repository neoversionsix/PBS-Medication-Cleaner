# import libraries
import pandas as pd
import numpy as np
import os
import pathlib as pth
import openpyxl as xl

# Input values
output = pth.Path('//whoffice/shared/EMR/BAU/Audit Spreadsheets/PBS audits/202105/Prescriber_type_20210501-consolidated-5.xlsx')
folder_1 = pth.Path('//whoffice/shared/EMR/BAU/Audit Spreadsheets/PBS audits/')
filename_excel = 'PBS Processing 5 - Medications_PBS_Mapping_Alignment_prodii.xlsx'
sheet_name_excel = 'prescriber type (from PBS text)'

# This will get the name of the folder we want
all_folder_names = os.listdir(folder_1)
folder_names = []
for item in all_folder_names:
    try:
        folder_names.append(int(item))
    except ValueError:
        continue

folder_names.sort(reverse=True)
folder = folder_names[0]
filename = 'Prescriber_type_' + str(folder) + '01' + '.txt'
file_loc_name = pth.Path.joinpath(folder_1, str(folder), filename)
file_loc_name = pth.PureWindowsPath(file_loc_name)
file_loc_name_excel = pth.Path.joinpath(folder_1, str(folder), filename_excel)

# Read the .txt document, wrangle and make the dataframe
column_names = ['desc', 'ID', 'role']
df_file = pd.read_csv(file_loc_name, sep = '\t', header=0, names = column_names)
df_file_out = df_file.drop_duplicates(subset='ID', keep=False)
unique_IDs = df_file_out['ID'].tolist()

for index, row in df_file.iterrows():
    id = df_file.loc[index]['ID']
    if id not in unique_IDs:
        df_temp = df_file[df_file['ID'] == id]
        roles = df_temp.role.tolist()
        roles = " ".join(roles)
        ser_temp = df_temp.iloc[0]
        ser_temp['role'] = roles
        df_file_out = df_file_out.append(ser_temp, ignore_index = True)
        unique_IDs.append(id)
    else:
        continue

# WRITE TO EXCEL SHEET
book = xl.load_workbook(file_loc_name_excel)
writer = pd.ExcelWriter(file_loc_name_excel, engine = 'openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
df_file_out.to_excel(writer, sheet_name_excel, index = False)
writer.save()

# Give user feedback
print('number of rows and columns:', df_file_out.shape)
print('all done!')
