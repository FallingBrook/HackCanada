import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.optimizers import Adam
import numpy as np
import matplotlib.pyplot as plt
import os
import sklearn.metrics

# Constants
IMG_SIZE = (512, 512)
BATCH_SIZE = 32
NUM_CLASSES = 3  # normal, benign, malignant
EPOCHS = 30


# Data Preparation
def create_generators(data_dir):
    train_datagen = ImageDataGenerator(
        rescale=1. / 255,
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        validation_split=0.2
    )

    train_generator = train_datagen.flow_from_directory(
        os.path.join(data_dir, 'train'),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    val_generator = train_datagen.flow_from_directory(
        os.path.join(data_dir, 'train'),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation'
    )

    test_datagen = ImageDataGenerator(rescale=1. / 255)

    test_generator = test_datagen.flow_from_directory(
        os.path.join(data_dir, 'test'),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False
    )

    return train_generator, val_generator, test_generator


# Model Architecture
def create_model():
    base_model = EfficientNetB0(
        include_top=False,
        weights='imagenet',
        input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)
    )
    base_model.trainable = False

    inputs = tf.keras.Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    x = base_model(inputs)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(256, activation='relu')(x)
    x = layers.Dropout(0.5)(x)
    outputs = layers.Dense(NUM_CLASSES, activation='softmax')(x)

    model = models.Model(inputs=inputs, outputs=outputs)

    model.compile(
        optimizer=Adam(learning_rate=1e-3),  # Corrected Import
        loss='categorical_crossentropy',
        metrics=['accuracy',
                 tf.keras.metrics.Precision(name='precision'),
                 tf.keras.metrics.Recall(name='recall')]
    )
    return model


# Training Function
def train_model(model, train_gen, val_gen):
    callbacks = [
        EarlyStopping(patience=5, restore_best_weights=True),
        ReduceLROnPlateau(factor=0.1, patience=3)
    ]

    history = model.fit(
        train_gen,
        epochs=EPOCHS,
        validation_data=val_gen,
        callbacks=callbacks
    )
    return history


# Evaluation Function
def evaluate_model(model, test_gen):
    results = model.evaluate(test_gen)
    print(f'Test Accuracy: {results[1] * 100:.2f}%')
    print(f'Test Precision: {results[2] * 100:.2f}%')
    print(f'Test Recall: {results[3] * 100:.2f}%')

    y_true = test_gen.classes
    y_pred = model.predict(test_gen).argmax(axis=1)

    class_names = list(test_gen.class_indices.keys())
    print('\nClassification Report:')
    print(sklearn.metrics.classification_report(y_true, y_pred, target_names=class_names))

    conf_matrix = sklearn.metrics.confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sklearn.metrics.ConfusionMatrixDisplay(conf_matrix, display_labels=class_names).plot()
    plt.title('Confusion Matrix')
    plt.show()


# Main Function
def main():
    data_path = os.path.abspath(os.getcwd()) + "\\dataset"
    train_gen, val_gen, test_gen = create_generators(data_path)
    model = create_model()
    history = train_model(model, train_gen, val_gen)
    evaluate_model(model, test_gen)
    model.save('cancer_classifier.h5')

    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train Accuracy')
    plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
    plt.title('Training History')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train Loss')
    plt.plot(history.history['val_loss'], label='Validation Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    main()
