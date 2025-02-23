import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt


def load_cancer_model(model_path):
    return tf.keras.models.load_model(model_path)


def preprocess_image(img_path, target_size=(512, 512)):
    img = image.load_img(img_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0  # Important: same scaling as training
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def predict_cancer(model, img_array, class_names):
    predictions = model.predict(img_array)
    predicted_class = np.argmax(predictions[0])
    confidence = np.max(predictions[0])
    return class_names[predicted_class], confidence



def checkForCancer(img_path):

    print("Processing results")

    # Load your trained model
    model = load_cancer_model('cancer_classifier.h5')

    # Define class names (must match your training setup)
    class_names = ['normal', 'benign', 'malignant']  # Replace if different

    # Preprocess and predict
    processed_img = preprocess_image(img_path)
    prediction, confidence = predict_cancer(model, processed_img, class_names)

    # # Show the image
    # img = image.load_img(img_path)
    # plt.imshow(img)
    # plt.title(f'{prediction} ({confidence:.2%})')
    # plt.axis('off')
    # plt.show()

    # Display results
    return f'Prediction: {prediction}' + f'  Confidence: {confidence:.2%}'