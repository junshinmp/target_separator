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

# gets record of preexisting batches in cloud
batches = project.get_batches()
made_batches = []
for batch in batches.get("batches", []):
    made_batches.append(batch.get("name"))

spliced_root = Path("raw_dataset")
if not spliced_root.exists():
    print(f"Error: '{spliced_root}' does not exist. Run video splicer first.")
    exit()

curr_count = 1
for video_dir in spliced_root.iterdir():
    print("\n---------------------------------------\n")
    if not video_dir.is_dir():
        print(f"{video_dir} is not a directory of images: skipping.")
        continue

    # check if the batch already exists within the cloud
    if video_dir.name in made_batches:
        print(f"{video_dir} already exists within the cloud, skipping.")
        continue

    print(f"Processing video #{curr_count}")
    print(f"    - Processing video: {video_dir.name}")
    for image in video_dir.iterdir():
        # check if valid image
        if image.name.startswith('.') or image.suffix.lower() not in ['.jpg', '.jpeg', '.png']:
            continue

        try:
            project.single_upload(
                image_path=str(image),
                batch_name=video_dir.name,
                num_retry_uploads=3
            )
            
        except Exception as e:
            print(f"        Error: Image {image} could not be uploaded to API")
    curr_count += 1

print(f"Finished uploading all images to cloud.")