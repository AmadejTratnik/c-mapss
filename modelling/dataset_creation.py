import pandas as pd

class DataSetMaker:
    def __init__(self, train_set: bool, path1: str, path2: str = None):
        self.train_set = train_set
        self.path1 = path1
        self.path2 = path2
        # Common column names
        self.column_names = ['unit_number', 'time', 'operational_setting_1', 'operational_setting_2', 'operational_setting_3']
        N = 24
        self.column_names += [f'sensor_measurement_{i}' for i in range(1, N)]

    def make_dataframe(self) -> pd.DataFrame:
        df = pd.read_csv(self.path1, sep=" ", header=None, names=self.column_names)
        # deleting empty columns
        df.dropna(how='all', axis=1, inplace=True)
        # delete duplicates
        df.drop_duplicates(inplace=True)
        
        if self.train_set:
            grouped_by = df.groupby(by='unit_number')
            max_time = grouped_by['time'].max()
            df = df.merge(max_time.to_frame(name='max_time'), left_on='unit_number', right_index=True)
            df['RUL'] = df['max_time'] - df['time']
            df['fault_detected'] = df.groupby('unit_number')['RUL'].transform(self.detect_fault)
            df.drop(columns=['RUL'], inplace=True)  # Drop the RUL column
        else:
            # Calculate fault_detected based on RUL ranges
            # Load RUL ranges from the second file
            rul_ranges = pd.read_csv(self.path2, sep=" ", header=None, names=['unit_number', 'rul_range'])
            # Merge the RUL ranges with the test dataframe
            df = df.merge(rul_ranges, on='unit_number')
            df['fault_detected'] = df['rul_range'].apply(self.detect_fault)
        
        return df

    @staticmethod
    def detect_fault(rul):
        warning = 0.7
        fault = 0.1
        if rul > warning:
            return 0  # Everything is ok
        elif rul > fault:
            return 1  # Warning
        else:
            return 2  # Fault detected

if __name__ == '__main__':
    # Example usage for training set
    train_set_maker = DataSetMaker(train_set=True, path1="../data/raw/train_FD001.txt")
    train_df = train_set_maker.make_dataframe()
    print(train_df)

    # Example usage for test set
    test_set_maker = DataSetMaker(train_set=False, path1="path_to_testing_file.txt", path2="path_to_rul_ranges.txt")
    test_df = test_set_maker.make_dataframe()
    print(test_df)