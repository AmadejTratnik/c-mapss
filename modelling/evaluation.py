from data_preprocess import get_train_test_data
import numpy as np
from tqdm import tqdm
from inference import load_jet_model, predict_fault
import seaborn as sns
import matplotlib.pyplot as plt


def evaluate_model_on_test_set(model, X, y) -> np.array:
    residual_matrix = []
    for sequence, target in tqdm(zip(X, y)):
        sequence = np.array([sequence])
        prediction = predict_fault(model, sequence)
        residual_matrix.append(prediction - np.argmax(target, axis=-1))
    return residual_matrix


def get_color_for_value(value):
    color_map = {
        -2: 'darkblue',
        -1: 'lightblue',
        0: 'white',
        1: 'lightred',
        2: 'darkred',
    }
    return color_map[value]


def save_evaluation_figure(jet, final_list):
    plt.figure(figsize=(10, 6))
    sns.heatmap(final_list, cbar=False,
                cmap="vlag")
    plt.title(f'Residuals for {jet}')
    plt.xlabel('Residual value')
    plt.ylabel('Unit')
    custom_tick_labels = ['-2', '-1', '0', '1', '2']
    plt.xticks(range(0, 5), custom_tick_labels)
    plt.savefig(f'./app/assets/{jet}_residuals.png')


def main():
    jets = ['FD001', 'FD002', 'FD003', 'FD004']
    for jet in jets:
        model = load_jet_model(f'./modelling/models/{jet}_model.keras')
        X_train, y_train, X_test, y_test = get_train_test_data(jet)
        residuals = evaluate_model_on_test_set(model, X_train, y_train)
        final_list = [count_residual_values(residual_vector) for residual_vector in residuals]
        save_evaluation_figure(jet, final_list)


def count_residual_values(residual_vector):
    value_counts = {-2: 0, -1: 0, 0: 0, 1: 0, 2: 0}
    for value in residual_vector:
        value_counts[value] += 1
    return list(value_counts.values())


if __name__ == '__main__':
    main()
