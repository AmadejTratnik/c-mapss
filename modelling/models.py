from keras import Input
import tensorflow as tf
from keras.src.regularizers import regularizers
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout


def create_model(input_shape,
                 num_classes):  # The input shape is specified as (None, 26) to handle sequences of variable lengths with 26 features.
    model = Sequential([
        Input(shape=input_shape),
        LSTM(32, return_sequences=True, recurrent_dropout=0.2),
        Dropout(0.3),
        Dense(32, activation='relu', kernel_regularizer=regularizers.L2(0.001)),  # L2 regularization on kernel weights
        LSTM(16, return_sequences=True, recurrent_dropout=0.2),
        Dropout(0.4),
        Dense(num_classes, activation='softmax')
    ])
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-4)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer,
                  metrics=['accuracy'])
    return model
