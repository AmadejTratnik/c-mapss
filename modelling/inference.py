import numpy as np
import sys

sys.path.append('.')


def load_jet_model(model_path):
    from keras.src.saving import load_model
    model = load_model(model_path)
    model.trainable = False
    return model


def predict_fault(model, new_x,verbose=False) -> int:
    return np.argmax(model.predict(new_x,verbose=int(verbose)), axis=-1)[0]


def generate_random_input_data(batch_size, time_steps, num_features):
    input_data = np.random.rand(batch_size, time_steps, num_features)
    return input_data


def init_models():
    model_fd001 = load_jet_model('./modelling/models/FD001_model.keras')
    model_fd002 = load_jet_model('./modelling/models/FD002_model.keras')
    model_fd003 = load_jet_model('./modelling/models/FD003_model.keras')
    model_fd004 = load_jet_model('./modelling/models/FD004_model.keras')
    return model_fd001, model_fd002, model_fd003, model_fd004


if __name__ == '__main__':
    model = load_jet_model('./modelling/models/FD001_model.keras')
    batch_size = 10
    time_steps = 500
    num_features = 24
    random_input_data = generate_random_input_data(batch_size, time_steps, num_features)
    prediction = predict_fault(model, random_input_data)
    print(prediction)
