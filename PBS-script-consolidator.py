# Input values
#region
file_loc_name = 'C:\\Users\\jason\\OneDrive\\Desktop\\data-out.xlsx'
excel_sheet = 'Sheet1'
output = 'C:\\Users\\jason\\OneDrive\\Desktop\\data-out-consolidated.xlsx'
#endregion

# import libraries
#region
import pandas as pd
import numpy as np
#endregion

# READ FILE and do stuff
#region
column_names = ['desc', 'ID', 'role']
df_file = pd.read_excel(file_loc_name, sheet_name=excel_sheet, header=None, names = column_names)
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
#endregion

# OUTPUT FILE
#region
df_file_out.to_excel(output, index=False)
print('all done!')
#endregion