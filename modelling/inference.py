import numpy as np


def load_jet_model(model_path):
    from keras.src.saving import load_model
    return load_model(model_path)


def predict_fault(model, current_measurement) -> int:
    prediction = model.predict(current_measurement, verbose=0)
    return np.argmax(prediction, axis=-1)[0][0]


def generate_random_input_data(batch_size, time_steps, num_features):
    input_data = np.random.rand(batch_size, time_steps, num_features)
    return input_data


if __name__ == '__main__':
    model = load_jet_model('FD001_model.keras')
    batch_size = 10
    time_steps = 500
    num_features = 24
    random_input_data = generate_random_input_data(batch_size, time_steps, num_features)
    prediction = predict_fault(model, random_input_data)
    print(prediction)
