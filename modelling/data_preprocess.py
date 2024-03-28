import pandas as pd
from sklearn.preprocessing import OneHotEncoder


def create_sequences(df):
    sequences = []
    targets = []
    encoder = OneHotEncoder(categories='auto')

    # Group data by 'unit'
    grouped = df.groupby('unit_number')

    for _, group in grouped:
        # Extract features and target variable
        X_sequence = group.drop(columns=['unit_number', 'time', 'fault_detected']).values
        y_sequence = group['fault_detected'].values.reshape(-1, 1)

        y_sequence_encoded = encoder.fit_transform(y_sequence).toarray()

        sequences.append(X_sequence)
        targets.append(y_sequence_encoded)

    return sequences, targets

def get_train_test_data(jet):
    train_df = read_df(jet,True)
    X_train, y_train = create_sequences(train_df)
    test_df = read_df(jet,False)
    X_test, y_test = create_sequences(test_df)
    return X_train,y_train,X_test,y_test


def read_df(jet,train=False):
    s = 'train' if train else 'test'
    df = pd.read_csv(f'../data/processed/{s}_{jet}.csv',)
    if 'Unnamed: 0' in df.columns:
        df.drop(columns=['Unnamed: 0'], inplace=True)
    df.sort_values(by=['unit_number', 'time'],inplace=True)
    return df

if __name__ == '__main__':
    df = read_df('FD001')
    X,y = create_sequences(df)
    print(y)