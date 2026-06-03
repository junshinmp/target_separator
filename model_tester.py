import os
import cv2
import glob
import torch
from pathlib import Path
from dotenv import load_dotenv
from roboflow import Roboflow
from ultralytics import YOLO

VERSION_NUMBER = 1
DATASET_CONFIG = "data.yaml"
device = "cuda" if torch.cuda.is_available() else "cpu" if 'torch' in globals() else "cpu"

load_dotenv()
API_KEY = os.getenv("ROBOFLOW_API_KEY")
PROJECT_ID = os.getenv("ROBOFLOW_PROJECT_ID")

if not API_KEY or not PROJECT_ID:
    print("Error: No Roboflow credientials utilized, check that your '.env' file is configured properly.")
    exit()

# uses the preexisting model, connecting to Roboflow's cloud
rf = Roboflow(api_key=API_KEY)
project = rf.workspace().project(PROJECT_ID)
version = project.version(VERSION_NUMBER)

# download the files temp
dataset = version.download("yolov8")

# in the newly created test file location, pull tester images
test_images = glob.glob(f"{dataset.location}/test/images/*.jpg")
print(f"Downloaded split. Found {len(test_images)} test images to evaluate.")

yolo = YOLO("yolov8n-p2.yaml").load("yolov8n.pt")
results = yolo.train(
    data=f"{dataset.location}/{DATASET_CONFIG}",
    epochs=5,
    imgsz=640, 
    box=12.0,            
    cls=2.5,              
    label_smoothing=0.05,
    batch=4,
    amp=True
)

best_model_path = "runs/detect/train/weights/best.pt"
trained_yolo = YOLO(best_model_path)

output_dir = Path("test_results")
output_dir.mkdir(exist_ok=True)

for img_path in test_images:
    filename = Path(img_path).name
    
    # Run inference on the test image
    predictions = trained_yolo(img_path, conf=0.10, verbose=False)
    
    # Extract details to print to the terminal
    for pred in predictions:
        boxes = pred.boxes
        print(f"Image: {filename} -- Found {len(boxes)} objects.")
        
        for box in boxes:
            class_id = int(box.cls[0].item())
            class_name = trained_yolo.names[class_id]
            confidence = box.conf[0].item()
            print(f"   - [{class_name.upper()}] Confidence: {confidence:.2f}")

        annotated_image = pred.plot()
        cv2.imwrite(str(output_dir / f"result_{filename}"), annotated_image)