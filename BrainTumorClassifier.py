from ultralytics import YOLO

# Load a model
model = YOLO("runs/detect/train/weights/best.pt")  # load a fine-tuned model

def checkForBrainTumor(img_path):
    # Inference using the model (img/video/stream)
    results = model.predict(img_path, save=True)

    return results[0].path
