import os
import pandas as pd


def get_files_with_prefix(directory_path, prefix_list):
    all_files = os.listdir(directory_path)
    filtered_files = sorted([file for file in all_files if any(file.startswith(prefix) for prefix in prefix_list)])       
    return filtered_files

def make_dataframe(text_file_path):
    column_names = ['unit_number','time','operational_setting_1','operational_setting_2','operational_setting_3']
    N =24 
    column_names += [f'sensor_measurement_{i}' for i in range(1,N)]
    df = pd.read_csv(text_file_path, sep=" ",header=None,names=column_names)
    # deleting empty columns
    df.dropna(how='all', axis=1, inplace=True) 
    #delete duplicates
    df.drop_duplicates(inplace=True)
    grouped_by = df.groupby(by='unit_number')
    max_time = grouped_by['time'].max()
    df = df.merge(max_time.to_frame(name='max_time'), left_on='unit_number', right_index=True)
    df['RUL'] = df['max_time'] - df['time']
    return df.to_dict('records')


if __name__ == '__main__':
    #print(get_files_with_prefix('./data/', ['test','train']))
    #print(make_dataframe('./data/'+'train_FD001.txt'))
    pass