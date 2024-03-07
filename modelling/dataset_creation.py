import pandas as pd

class DataSetMaker:
    def __init__(self,train_set:bool, path1:str, path2:str=None):
        self.train_set = train_set
        self.path1 = path1
        self.path2 = path2

    def make_dataframe(self) -> bool:
        if self.train_set:
            data = pd.read_csv(self.path1)
    

if __name__ == '__main__':
    s = DataSetMaker(True,"a").make_dataframe()
    print(s)



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