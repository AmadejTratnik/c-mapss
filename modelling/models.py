from keras import Input
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import LSTM, Dense

# Define the model architecture
def create_model(input_shape, num_classes): # The input shape is specified as (None, 26) to handle sequences of variable lengths with 26 features.
    model = Sequential([
        Input(shape=input_shape),
        LSTM(64, return_sequences=True),
        LSTM(64, return_sequences=True),
        Dense(64, activation='relu'),
        Dense(num_classes, activation='softmax')
    ])
    optimizer = tf.keras.optimizers.Adam(learning_rate=1e-3)
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
    return model