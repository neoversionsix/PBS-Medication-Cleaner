# Input values
#region
file_loc_name = 'C:\\Users\\jason\\OneDrive\\Desktop\\data.xlsx'
excel_sheet = 'PBS'
output = 'C:\\Users\\jason\\OneDrive\\Desktop\\data-out.xlsx'
#endregion


# import libraries
#region
import pandas as pd
import numpy as np
#endregion

# READ FILE and do stuff
column_names = ['desc', 'ID', 'role']
df_file = pd.read_excel(file_loc_name, sheet_name=excel_sheet, header=None, names = column_names)
df_file_out = pd.DataFrame(columns=column_names)

for index, row in df_file.iterrows():
    if ' ' in row['role']:
        roles_str = df_file.loc[index]['role']
        roles_lst = roles_str.split(' ')
        for x in roles_lst:
            df_temp = df_file.iloc[index]
            df_temp['role'] = x
            df_file_out=df_file_out.append(df_temp, ignore_index=True)
    else:
        df_file_out=df_file_out.append(df_file.iloc[index], ignore_index=True)
        

# OUTPUT FILE
#region
df_file_out.to_excel(output, index=False)
print('all done!')
#endregion
