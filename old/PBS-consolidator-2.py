print('------------------------------------------------------------------------')
print('INFO')
print('------------------------------------------------------------------------')
print('Make sure you have created the folder in [//whoffice/shared/EMR/BAU/Audit Spreadsheets/PBS audits/]. The folder name in there should be like this [YYYYYMM].')
print('Inside the folder [YYYYYMM] place the file [Prescriber_type_YYYYMM01.txt].')
print('If that is not done please close this window and do that first.')
print('Have you put the file [Prescriber_type_YYYYMM01.txt] in the folder? enter y for yes, otherwise close this window.')
print('------------------------------------------------------------------------')
print('QUESTION')
print('Have you put the file [Prescriber_type_YYYYMM01.txt] in the folder? enter y for yes, otherwise close this window.')
inp = input('enter "y" (then enter) to continue or close the window: ')
print('-------------------------------------------------------------------------')
print('LAST QUESTION')
print('Have you put the xlsx files from "Spreadsheets" in the "[YYYYYMM]" folder? enter y for yes, otherwise close this window.')
inp = input('enter "y" to continue or close the window: ')
print('-------------------------------------------------------------------------')

# import libraries
print('RUNNING SCRIPT AND PROCESSING DATA')
print('------------------------------------------------------------------------')
print('Computer: I am now doing stuff. This whole thing should take less than 5 mins.')
import pandas as pd
import os
import pathlib as pth
import openpyxl as xl
print('- Libraries imported')


# Input values
folder_0 = r'//whoffice/shared/EMR/BAU/Audit Spreadsheets/PBS audits'
folder_1 = pth.Path(folder_0)
folder_spreadsheets = r'//whoffice/shared/EMR/BAU/Audit Spreadsheets/PBS audits/Spreadsheets'
filename_excel = 'PBS Processing 5 - Medications_PBS_Mapping.xlsx'
sheet_name_excel = 'prescriber type (from PBS text)'
print('- folder path: //whoffice/shared/EMR/BAU/Audit Spreadsheets/PBS audits/Spreadsheets')
print('- excel file to target: PBS Processing 5 - Medications_PBS_Mapping.xlsx')
print('- sheet name to target: prescriber type (from PBS text)')

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
print('- reading text file')
df_file = pd.read_csv(file_loc_name, sep = '\t', header=0, names = column_names)
df_file_out = df_file.drop_duplicates(subset='ID', keep=False)
unique_IDs = df_file_out['ID'].tolist()
print('- processing text file...')

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
print('done processing text file')

# WRITE TO EXCEL SHEET
print('- writing data to the spreadsheet...')
book = xl.load_workbook(file_loc_name_excel)
del book[sheet_name_excel]
writer = pd.ExcelWriter(file_loc_name_excel, engine = 'openpyxl')
writer.book = book
writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
df_file_out.to_excel(writer, sheet_name_excel, index = False)
print('- saving excel file (be patient)...')
writer.save()
print('- file saved')

# Give user feedback
print('- number of rows and columns:', df_file_out.shape)
print('- all done!')
print('------------------------------------------------------------------------')
print('YOU CAN NOW CLOSE')
print('------------------------------------------------------------------------')