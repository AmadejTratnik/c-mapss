import numpy as np
from data_preprocess import get_train_test_data
from models import create_model


def train_model_individual_sequences(model, sequences, targets, epochs=10, validation_data=None):
    train_losses = []
    train_accuracies = []
    val_losses = []
    val_accuracies = []
    for epoch in range(1, epochs + 1):
        total_loss = 0
        total_accuracy = 0
        for X_sequence, y_sequence in (zip(sequences, targets)):
            X_sequence = np.array([X_sequence])
            y_sequence = np.array([y_sequence])

            # Train on the individual sequence
            history = model.fit(X_sequence, y_sequence, epochs=1, batch_size=1, verbose=0)
            total_loss += history.history['loss'][0]
            total_accuracy += history.history['accuracy'][0]

        # Calculate average loss and accuracy
        avg_loss = total_loss / len(sequences)
        avg_accuracy = total_accuracy / len(sequences)

        # Print epoch summary
        print(f"Epoch {epoch}/{epochs} - Loss: {avg_loss:.4f} - Accuracy: {avg_accuracy:.4f}")
        train_losses.append(avg_loss)
        train_accuracies.append(avg_accuracy)
        if validation_data:
            flat_validation_data_x = np.concatenate(validation_data[0], axis=0)
            flat_validation_data_y = np.concatenate(validation_data[1], axis=0)

            np_validation_data_x = flat_validation_data_x.reshape(-1, 1, flat_validation_data_x.shape[1])
            np_validation_data_y = flat_validation_data_y.reshape(-1, 1, flat_validation_data_y.shape[1])
            val_loss, val_accuracy = model.evaluate(np_validation_data_x, np_validation_data_y, verbose=0)
            val_losses.append(val_loss)
            val_accuracies.append(val_accuracy)

            print(f" - Val Loss: {val_loss:.4f} - Val Accuracy: {val_accuracy:.4f}")
    return model, train_losses, train_accuracies,val_losses,val_accuracies


def save_model(model, filename):
    model.save(filename)


def main():
    jet = 'FD001'
    EPOCHS = 130
    X_train, y_train, X_test, y_test = get_train_test_data(jet)
    input_shape = (None, X_train[0].shape[1])
    num_classes = y_train[0].shape[1]
    model = create_model(input_shape, num_classes)
    validation_data = (X_test, y_test)
    trained_model, train_losses, train_accuracies,val_losses,val_accuracies = train_model_individual_sequences(model, X_train, y_train, epochs=EPOCHS,
                                                                       validation_data=validation_data)
    save_model(trained_model, f"{jet}_model.keras")

    import matplotlib.pyplot as plt
    plt.figure(figsize=(10, 6))

    plt.plot(range(EPOCHS), train_losses, label='Training Loss')
    plt.plot(range(EPOCHS), train_accuracies, label='Training Accuracy')
    plt.plot(range(EPOCHS), val_losses, label='Validation Loss')
    plt.plot(range(EPOCHS), val_accuracies, label='Validation Accuracy')
    plt.title(f'Losses and Accuracies for {jet}')
    plt.xlabel('Epoch')
    plt.ylabel('Loss/Accuracy')
    plt.legend()
    plt.savefig('losses_and_accuracies.png')  # Adjust file name as needed


if __name__ == '__main__':
    main()
