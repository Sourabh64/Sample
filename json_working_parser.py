import json
import time
import pandas as pd

start = time.time()
with open('nw_report.json', 'r', encoding='utf8') as f:
    data = json.load(f)


# def flatten_data(y):
#     out = {}
#     path_list = []
#
#     def flatten(x, path='root'):
#         if type(x) is dict:
#             for a in x:
#                 flatten(x[a], path + a )
#         elif type(x) is list:
#             i = 0
#             for a in x:
#                 flatten(a, path + '#')
#                 i += 1
#         else:
#             if path[:-1] in out.keys():
#                 out[path[:-1]].append(x)
#             else:
#                 path_list.append(path[:])
#                 out[path[:-1]] = [x]
#
#     flatten(y)
#     return out
col_list = []
df_dict = {}
# del_col_dict = {}
# del_col_list = []


def normalize_json(data_list):
    df = pd.json_normalize(data_list)
    for col in df.columns:
        if col not in col_list:
            col_list.append(col)
    return df


def data_frame_append(df_data, path, old_path=None, key=None):
    df = df_data
    if path in df_dict:
        df_dict[f'{path}'] = pd.concat([df_dict[f'{path}'], df], axis=0)
        if old_path:
            if key in df_dict[f'{old_path}'].columns:
                df_dict[f'{old_path}'].drop(key, axis=1, inplace=True)
        else:
            pass
    else:
        df_dict[f'{path}'] = df_data


# def delete_columns(key, old_path):
#     if old_path:
#         if old_path not in del_col_dict:
#             del_col_list = [key]
#             del_col_dict[f'{old_path}'] = del_col_list
#         else:
#             if key not in del_col_dict[f'{old_path}']:
#                 del_col_list.append(key)
#                 del_col_dict[f'{old_path}'] = del_col_list
#             else:
#                 pass


def process_data(data):
    parent_key = 0
    current_key = 0
    for each in data:
        parent_key += 1

        def flatten(new_data, path='root_nw_report'):
            if isinstance(new_data, dict):
                for key in new_data:
                    if isinstance(new_data[key], list) and new_data[key]:
                        internal_df = normalize_json(new_data[key])
                        internal_df['parent_key'] = parent_key
                        data_frame_append(internal_df, path+"_"+key, path, key)
                        # delete_columns(key, path)
                        flatten(new_data[key], path+"_"+key)
            if isinstance(new_data, list) and new_data:
                for key in new_data:
                    if isinstance(key, dict):
                        flatten(key, path)

        flatten(each)


data_frame = normalize_json(data)
data_frame['parent_key'] = range(1, 1+len(data_frame))
data_frame_append(data_frame, 'root_nw_report')
process_data(data)

count = 0
# print(del_col_dict)
# print(df_dict)
# for i in del_col_dict:
#     for j in del_col_dict[i]:
#         df_dict[i].drop(j, axis=1, inplace=True)
# print(df_dict)
for i in df_dict:
    count += 1
    df_dict[i].to_csv(f'csvs/{i}.csv')
print(time.time() - start)
# print(col_list)
# print(len(col_list))
# print(output)
