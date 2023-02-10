""" 해구정보 텍스트 라인 핸들링 """
'''
new_lines = []
with open('C:/Users/Joel/Desktop/trench.txt', 'r+', encoding='utf-8') as f:
    rows = f.readlines()
    line_string = ''
    for row, idx in zip(rows, range(len(rows))):
        if (idx + 1) % 3 != 0:
            line_string += row[:-1] + '\t'
        elif (idx + 1) % 3 == 0:
            line_string += row
            new_lines.append(line_string)
            line_string = ''
    f.close()

with open('C:/Users/Joel/Desktop/trench_mod.txt', 'w+', encoding='utf-8') as f:
    f.writelines(new_lines)
    f.close()
'''
import pandas as pd

f = pd.read_csv('marine_zone.csv', encoding='utf-8', index_col=['IDX'])
# print(f)
cols = f.columns
idxs = f.index

new_table = pd.DataFrame(columns=cols)
for idx in idxs:
    ul_lon = f.loc[idx]['UPPER_LEFT_LONGITUDE']
    ul_lat = f.loc[idx]['UPPER_LEFT_LATITUDE']
    new_table.loc['Z' + str(idx) + 'S11'] = [ul_lon, ul_lat,
                                             ul_lon + 0.25, ul_lat,
                                             ul_lon + 0.25, ul_lat - 0.25,
                                             ul_lon, ul_lat - 0.25]
    new_table.loc['Z' + str(idx) + 'S12'] = [ul_lon + 0.25, ul_lat,
                                             ul_lon + 0.5, ul_lat,
                                             ul_lon + 0.5, ul_lat - 0.25,
                                             ul_lon + 0.25, ul_lat - 0.25]
    new_table.loc['Z' + str(idx) + 'S21'] = [ul_lon, ul_lat - 0.25,
                                             ul_lon + 0.25, ul_lat - 0.25,
                                             ul_lon + 0.25, ul_lat - 0.5,
                                             ul_lon, ul_lat - 0.5]
    new_table.loc['Z' + str(idx) + 'S22'] = [ul_lon + 0.25, ul_lat - 0.25,
                                             ul_lon + 0.5, ul_lat - 0.25,
                                             ul_lon + 0.5, ul_lat - 0.5,
                                             ul_lon + 0.25, ul_lat - 0.5]

new_table = new_table.reset_index()
new_table = new_table.rename(columns={'index': 'GRID_NAME'})


# new_table.to_csv('Zone_Sector.csv', encoding='cp949')

mof_sector = pd.read_csv('POLYGON_PROCESSED_DATA.csv')
# tpx_sector = pd.read_csv('Zone_Sector.csv')
#
# merge_outer = pd.merge(tpx_sector, mof_sector, how='outer', on=['UPPER_LEFT_LONGITUDE', 'UPPER_LEFT_LATITUDE', 'UPPER_RIGHT_LONGITUDE', 'UPPER_RIGHT_LATITUDE', 'LOWER_RIGHT_LONGITUDE', 'LOWER_RIGHT_LATITUDE', 'LOWER_LEFT_LONGITUDE', 'LOWER_LEFT_LATITUDE'])
merge_outer = pd.merge(mof_sector, new_table, how='left', on=['UPPER_LEFT_LONGITUDE', 'UPPER_LEFT_LATITUDE', 'UPPER_RIGHT_LONGITUDE', 'UPPER_RIGHT_LATITUDE', 'LOWER_RIGHT_LONGITUDE', 'LOWER_RIGHT_LATITUDE', 'LOWER_LEFT_LONGITUDE', 'LOWER_LEFT_LATITUDE'])
merge_outer.to_csv('GRID_left_join_on_MOF.csv', encoding='cp949')