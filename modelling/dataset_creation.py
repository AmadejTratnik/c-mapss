import pandas as pd

class DataSetMaker:
    def __init__(self, train_set: bool, path1: str, path2: str = None,warning: float = 0.7, fault: float = 0.1):
        self.train_set = train_set
        self.path1 = path1
        self.path2 = path2
        self.warning =warning
        self.fault = fault
        # Common column names
        self.column_names = ['unit_number', 'time', 'operational_setting_1', 'operational_setting_2', 'operational_setting_3']
        N = 24
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

                df['RUL'] += [rul_test_values[unit_num-1] for unit_num in df['unit_number']]
        
        df['fault_detected'] = df.groupby('unit_number')['RUL'].transform(self.detect_fault)

        df.drop(columns=['RUL','max_time'], inplace=True)
        return df

    def detect_fault(self,rul):

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

    train_set_maker = DataSetMaker(train_set=True, path1="./data/raw/train_FD001.txt")
    train_df = train_set_maker.make_dataframe()

    test_set_maker = DataSetMaker(train_set=False, path1="./data/raw/test_FD001.txt", path2='./data/raw/RUL_FD001.txt')
    test_df = test_set_maker.make_dataframe()

    train_distribution = train_df.groupby('unit_number')['fault_detected'].value_counts(normalize=True).unstack(fill_value=0)
    print("Train Dataset Distribution:")
    print(train_distribution)

    # For test dataset
    test_distribution = test_df.groupby('unit_number')['fault_detected'].value_counts(normalize=True).unstack(fill_value=0)
    print("\nTest Dataset Distribution:")
    print(test_distribution)

    import seaborn as sns
    import matplotlib.pyplot as plt
    import numpy as np
   
    train_percentiles = np.percentile(train_df["fault_detected"], np.linspace(0, 100, 101))
    test_percentiles = np.percentile(test_df["fault_detected"], np.linspace(0, 100, 101))

    # Create the plot
    plt.plot(train_percentiles, test_percentiles, linestyle='-', marker='o', label='Q-Q Plot')

    # Add diagonal line for reference
    plt.plot([0, 1], [0, 1], color='red', linestyle='--', label='Ideal Distribution')

    # Set labels and title
    plt.xlabel("Quantiles (Train)")
    plt.ylabel("Quantiles (Test)")
    plt.title("Custom Q-Q Plot for Fault Detection Distribution")
    plt.legend()
    plt.tight_layout()
    plt.savefig("fault_distribution.png")  # Replace with desired filename and format