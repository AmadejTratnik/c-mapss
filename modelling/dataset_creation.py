import argparse
import os
import pandas as pd
import sys

sys.path.append('.')
from app.data_access import get_files_with_prefix


def make_processed_data(raw_data_path='../data/raw/', proc_repo='../data/processed/', warning=0.7, fault=0.1):
    train_paths = get_files_with_prefix(raw_data_path, ['train'])
    test_paths = get_files_with_prefix(raw_data_path, ['test'])
    rul_paths = get_files_with_prefix(raw_data_path, ['RUL'])

    print("Generating training data...")
    for i, path in enumerate(train_paths):
        final_path = f'train_FD00{i + 1}.csv'
        df = DataSetMaker(train_set=True, path1=path, warning=warning, fault=fault).make_dataframe()
        df.to_csv(proc_repo + final_path)

    print("Generating testing data...")
    for i, (path1, path2) in enumerate(zip(test_paths, rul_paths)):
        final_path = f'test_FD00{i + 1}.csv'
        df = DataSetMaker(train_set=True, path1=path1, path2=path2, warning=warning, fault=fault).make_dataframe()
        df.to_csv(proc_repo + final_path)

    print("The end.")


class DataSetMaker:
    def __init__(self, train_set: bool, path1: str, path2: str = None, warning: float = 0.7, fault: float = 0.1):
        N = 24
        self.train_set = train_set
        self.path1 = path1
        self.path2 = path2
        self.warning = warning
        self.fault = fault

        self.column_names = ['unit_number', 'time', 'operational_setting_1', 'operational_setting_2',
                             'operational_setting_3']
        self.column_names += [f'sensor_measurement_{i}' for i in range(1, N)]

    def make_dataframe(self) -> pd.DataFrame:
        df = pd.read_csv(self.path1, sep=" ", header=None, names=self.column_names)
        df.dropna(how='all', axis=1, inplace=True)
        df.drop_duplicates(inplace=True)

        grouped_by = df.groupby(by='unit_number')
        max_time = grouped_by['time'].max()
        df = df.merge(max_time.to_frame(name='max_time'), left_on='unit_number', right_index=True)
        df['RUL'] = df['max_time'] - df['time']

        if not self.train_set:
            if self.path2 is not None:
                with open(self.path2, 'r') as file:
                    rul_test_values = [int(line.strip()) for line in file]

                df['RUL'] += [rul_test_values[unit_num - 1] for unit_num in df['unit_number']]

        df['fault_detected'] = df.groupby('unit_number')['RUL'].transform(self.detect_fault)

        df.drop(columns=['RUL', 'max_time'], inplace=True)
        return df

    def detect_fault(self, rul):

        if isinstance(rul, pd.Series):
            total_cycles = rul.max()  # Maximum cycle for the unit
            threshold_warning = self.warning * total_cycles
            threshold_fault = self.fault * total_cycles

            def fault_detection(val):
                if val > threshold_warning:
                    return 0  # Everything is ok
                elif val > threshold_fault:
                    return 1  # Warning
                else:
                    return 2  # Fault detected

            return rul.apply(fault_detection)
        elif isinstance(rul, int) or isinstance(rul, float):
            if rul > self.warning:
                return 0  # Everything is ok
            elif rul > self.fault:
                return 1  # Warning
            else:
                return 2  # Fault detected
        else:
            raise ValueError("Invalid input type for 'rul'. It should be either int, float, or pd.Series.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process data from raw to processed format.")
    parser.add_argument("--warning", type=float, default=0.66,
                        help="Threshold for warning condition (default: 0.66).")
    parser.add_argument("--fault", type=float, default=0.33,
                        help="Threshold for fault condition (default: 0.33).")
    args = parser.parse_args()
    make_processed_data('./data/raw/', './data/processed/', warning=args.warning, fault=args.fault)
    pass
