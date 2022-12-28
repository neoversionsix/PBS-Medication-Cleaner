# import libraries
import pandas as pd

#filename_sing 5 - Medications_PBS_Mapping_Alignment_prodii.xlsx'
#sheet_name_excel = 'prescriber type (from PBS text
file_loc_name = r'D:\DOWNLOADS\Prescriber_type_20210601.txt'

# Read the .txt document, wrangle and make the dataframe
column_names = ['desc', 'ID', 'role']
df_file = pd.read_csv(file_loc_name, sep = '\t', header=0, names = column_names)
df_file_out = df_file.drop_duplicates(subset='ID', keep=False)
unique_IDs = df_file_out['ID'].tolist()

print('consolidating data')
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
df_file_out.to_excel(r'D:\DOWNLOADS\PBS-out.xlsx', index = False)


# Give user feedback
print('number of rows and columns:', df_file_out.shape)
print('all done!')