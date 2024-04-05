import time

import numpy as np
from data_preprocess import get_train_test_data
from models import create_model


def train_model_individual_sequences(model, sequences, targets, X_test, y_test, epochs, patience=4):
    best_val_loss = np.inf  # implementing early stopping, if validation loss doesnt get any better
    early_stopping_count = 0
    train_losses = []
    train_accuracies = []
    val_losses = []
    val_accuracies = []
    L = len(list(X_test))
    for epoch in range(1, epochs + 1):

        total_loss = 0
        total_accuracy = 0
        for X_sequence, y_sequence in (zip(sequences, targets)):
            X_sequence = np.array([X_sequence])
            y_sequence = np.array([y_sequence])

            history = model.fit(X_sequence, y_sequence, epochs=1, batch_size=1, verbose=0)
            total_loss += history.history['loss'][0]
            total_accuracy += history.history['accuracy'][0]

        avg_loss = total_loss / len(sequences)
        avg_accuracy = total_accuracy / len(sequences)

        print(f"Epoch {epoch}/{epochs} - Loss: {avg_loss:.4f} - Accuracy: {avg_accuracy:.4f}")
        train_losses.append(avg_loss)
        train_accuracies.append(avg_accuracy)

        if X_test:
            val_loss = 0
            val_accuracy = 0
            for val_X, val_y in zip(X_test, y_test):
                val_X_sequence = np.array([val_X])
                val_y_sequence = np.array([val_y])
                predictions = model.predict(val_X_sequence, verbose=0)
                batch_accuracy = np.mean(np.argmax(predictions, axis=-1) == np.argmax(val_y_sequence, axis=-1))
                val_accuracy += batch_accuracy
                batch_loss = -np.mean(np.sum(val_y_sequence * np.log(predictions), axis=-1))
                val_loss += batch_loss
                # print(f"    - Batch loss: {batch_loss} -> batch accuracy {batch_accuracy}")

            avg_val_loss = val_loss / L
            avg_val_accuracy = val_accuracy / L
            val_losses.append(avg_val_loss)
            val_accuracies.append(avg_val_accuracy)
            print(f" - Val Loss: {avg_val_loss:.4f} - Val Accuracy: {avg_val_accuracy:.4f}")

            if avg_val_loss < best_val_loss:
                best_val_loss = avg_val_loss
                early_stopping_count = 0
            else:
                early_stopping_count += 1

            if early_stopping_count >= patience:
                print("Early stopping triggered!")
                break
    return model, train_losses, train_accuracies, val_losses, val_accuracies


def save_model(model, filename):
    model.save(filename)


def save_fig(jet, epochs, train_losses, train_accuracies, val_losses=None, val_accuracies=None):
    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))

    epochs = min(epochs, len(train_losses))  # early stopping validation

    plt.plot(range(epochs), train_losses, label='Training Loss')
    plt.plot(range(epochs), train_accuracies, label='Training Accuracy')
    if val_losses:
        plt.plot(range(epochs), val_losses, label='Validation Loss')
    if val_accuracies:
        plt.plot(range(epochs), val_accuracies, label='Validation Accuracy')
    plt.title(f'Losses and Accuracies for {jet}')
    plt.xlabel('Epoch')
    plt.ylabel('Loss/Accuracy')
    plt.legend()
    plt.savefig(f'../app/assets/{jet}_losses_and_accuracies.png')


def main():
    jets = 'FD001','FD002','FD003','FD004'
    for jet in jets:
        EPOCHS = 100
        X_train, y_train, X_test, y_test = get_train_test_data(jet)
        input_shape = (None, X_train[0].shape[1])
        num_classes = y_train[0].shape[1]
        model = create_model(input_shape, num_classes)
        trained_model, train_losses, train_accuracies, val_losses, val_accuracies = train_model_individual_sequences(
            model,
            X_train,
            y_train,
            X_test,
            y_test,
            epochs=EPOCHS,
            patience=20)
        print(f"For jet {jet} we got to {len(train_losses)} epochs")
        save_model(trained_model, f"models/{jet}_model.keras")
        save_fig(jet, EPOCHS, train_losses, train_accuracies, val_losses, val_accuracies)

if __name__ == '__main__':
    main()
