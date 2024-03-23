import os
import pandas as pd


def get_files_with_prefix(directory_path: str, prefix_list: list) -> list[str]:
    all_files = os.listdir(directory_path)
    filtered_files = sorted(
        [directory_path + file for file in all_files if any(file.startswith(prefix) for prefix in prefix_list)])
    return filtered_files


def get_dataframe(value: str) -> dict:
    return pd.read_csv(value).to_dict('records')


if __name__ == '__main__':
    print(get_files_with_prefix('./data/', ['test', 'train']))
    # print(make_dataframe('./data/'+'train_FD001.txt'))
    pass
