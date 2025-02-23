from ultralytics import YOLO

# Load a model
model = YOLO("yolo11n.pt")  # load a fine-tuned model

# Inference using the model (img/video/stream)
results = model.predict("https://ultralytics.com/assets/brain-tumor-sample.jpg", save=True)