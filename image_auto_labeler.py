import os
import cv2
import os
import time
import subprocess
import video_splicer
import image_uploader

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

# tracking variables for statistical info
total_result_frames = 0
total_time = 0
times_per_split = {}
frame_count = 0
saved_count = 0
out_path = ""

# Path files for the helper files:
IMAGE_UPLOADER = Path(image_uploader.py)
VIDEO_SPLICER = Path(video_splicer.py)

# first splice up all the videos into multiple images


# second upload all the images into the cloud:

# third now we use the pre-existing model in order to autolabel the new training data

# produce statistical information
