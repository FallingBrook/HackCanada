import time

from ultralytics import YOLO

# Load a model
model = YOLO("runs/detect/train/weights/best.pt")  # load a fine-tuned model

def checkForBrainTumor(img_path):

    print(img_path)
    name = img_path.split("\\")[-1]
    print(name)
    # Ensure the path uses forward slashes and no leading slash (adjust as needed)
    results = model.predict(
        img_path,
        save=True,
        project="static",                 # Parent directory (e.g., "static")
        name="BrainTumorPredictions",     # Subdirectory name
        exist_ok=True,                   # Overwrite existing files/folders
        max_det=1
    )

    # time.sleep(20)



    return name  # Returns the actual save directory used

# print(checkForBrainTumor("BrainTumorTestData\\tumor.jpg"))
