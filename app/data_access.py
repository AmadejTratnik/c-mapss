import os
import pandas as pd


def get_files_with_prefix(directory_path, prefix_list):
    all_files = os.listdir(directory_path)
    filtered_files = sorted([directory_path+file for file in all_files if any(file.startswith(prefix) for prefix in prefix_list)])       
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
    df['fault_detected'] = df.groupby('unit_number')['RUL'].transform(detect_fault)
    return df.to_dict('records')

def detect_fault(series):
    warning = 0.7
    fault = 0.1
    total_cycles = series.max()  # Maximum cycle for the unit
    threshold_warning = warning * total_cycles
    threshold_fault = fault * total_cycles
    
    def fault_detection(rul):
        if rul > threshold_warning:
            return 0  # Everything is ok
        elif rul > threshold_fault:
            return 1  # Warning
        else:
            return 2  # Fault detected
    
    return series.apply(fault_detection)


if __name__ == '__main__':
    print(get_files_with_prefix('./data/', ['test','train']))
    #print(make_dataframe('./data/'+'train_FD001.txt'))
    pass