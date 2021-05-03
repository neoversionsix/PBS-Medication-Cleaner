# import libraries
import pandas as pd
import numpy as np
from pathlib import Path, PureWindowsPath

# Input values
file_loc_name = Path('//whoffice/shared/EMR/BAU/Audit Spreadsheets/PBS audits/202105/Prescriber_type_20210501.txt')
file_loc_name = PureWindowsPath(file_loc_name)
output = Path('C:/PBS/x-out-3.xlsx')

# READ FILE and do stuff
column_names = ['desc', 'ID', 'role']
df_file = pd.read_csv(file_loc_name, sep = '\t', header=None, names = column_names, engine='python')
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


# OUTPUT FILE
df_file_out.to_excel(output, index=False)
print('all done!')
