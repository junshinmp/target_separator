import os
import cv2
import glob
import torch
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
from roboflow import Roboflow
from ultralytics import YOLO

VERSION_NUMBER = 1
DATASET_CONFIG = "data.yaml"

if __name__ == '__main__':
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    if torch.cuda.is_available():
        device = "0"
        print(f"GPU being used: {torch.cuda.get_device_name(0)}")
    else: 
        device = "cpu" 
        print("GPU not found, using CPU.")

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
    dataset = version.download("yolov8")

    # in the newly created test file location, pull tester images
    test_images = glob.glob(f"{dataset.location}/test/images/*.jpg")
    test_images.sort()
    print(f"Downloaded split. Found {len(test_images)} test images to evaluate.")

    yolo = YOLO("yolov8n-p2.yaml").load("yolov8n.pt")
    results = yolo.train(
        data=f"{dataset.location}/{DATASET_CONFIG}",
        device=device,
        epochs=10,
        imgsz=640, 
        box=12.0,            
        cls=2.5,
        label_smoothing=0.05,
        batch=4,
        amp=True,
        exist_ok=True
    )
    
    freshest_run_dir = Path(yolo.trainer.save_dir) # type: ignore
    
    best_path = freshest_run_dir / "weights" / "best.pt"
    last_path = freshest_run_dir / "weights" / "last.pt"
    
    # Select whichever weight file actually exists in that folder
    best_model_path = best_path if best_path.exists() else last_path

    print(f"\n🎯 Target Locked! Loading custom weights from: {best_model_path}")
    trained_yolo = YOLO(str(best_model_path))

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