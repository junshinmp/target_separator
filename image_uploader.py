import os
from pathlib import Path
from roboflow import Roboflow
from dotenv import load_dotenv

# uses dotenv to hide api key
load_dotenv()
API_KEY = os.getenv("ROBOFLOW_API_KEY")
PROJECT_ID = os.getenv("ROBOFLOW_PROJECT_ID")

if not API_KEY or not PROJECT_ID:
    print("Error: No Roboflow credientials utilized, check that your '.env' file is configured properly.")
    exit()

# uses the preexisting model, connecting to Roboflow's cloud
rf = Roboflow(api_key=API_KEY)
project = rf.workspace().project(PROJECT_ID)

spliced_root = Path("raw_dataset")
if not spliced_root.exists():
    print(f"Error: '{spliced_root}' does not exist. Run video splicer first.")
    exit()

for video_dir in spliced_root.iterdir():
    print("\n---------------------------------------\n")
    if not video_dir.is_dir():
        continue

    for image in video_dir.iterdir():
        print(f"    - Processing image: {image}")
        try:
            project.single_upload(
                image_path=str(image),
                batch_name=video_dir.name,
                num_retry_uploads=3
            )
            
        except Exception as e:
            print(f"        Error: Image {image} could not be uploaded to API")

print(f"Finished uploading all images to cloud.")