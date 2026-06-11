import os
import cv2
import glob
import torch
from pathlib import Path
from dotenv import load_dotenv
from roboflow import Roboflow
from ultralytics import YOLO

# Setting Parameters
API_KEY = None
PROJECT_ID = None
DEVICE = None
RF = None
PROJECT = None
VERSION = None
VERSION_NUMBER = 1
DATASET_CONFIG = "data.yaml"

class AimTrainingAnalysis(L.LightingModule):
    def __init__(self):
        print("Nothing")

    def lstm_unit(self, input_value, long_memory, short_memory):
        print("Nothing")

def print_parameters():
    print(f"API_KEY: {API_KEY}")
    print(f"PROJECT_ID: {PROJECT_ID}")
    print(f"DEVICE: {DEVICE}")
    print(f"ROBOFLOW: {RF}")
    print(f"PROJECT: {PROJECT}")
    print(f"VERSION: {VERSION}")
    print(f"VERSION_NUMBER: {VERSION_NUMBER}")

def environment_load():
    print("Loading Environment:\n")

    print("Setting Model usage as GPU or CPU.")
    os.environ["CUDA_VISIBLE_DEVICES"] = "0"
    if torch.cuda.is_available():
        DEVICE = 0
        print(f"GPU being used: {torch.cuda.get_device_name(0)}")
    else: 
        DEVICE = "cpu" 
        print("GPU not found, using CPU.")

    print("Loading from environment file.")
    load_dotenv()
    API_KEY = os.getenv("ROBOFLOW_API_KEY")
    PROJECT_ID = os.getenv("ROBOFLOW_PROJECT_ID")

    if not API_KEY or not PROJECT_ID:
        print("Error: No Roboflow credientials utilized, check that your '.env' file is configured properly.")
        exit()

    print("Connecting to Roboflow's cloud.")
    RF = Roboflow(api_key=API_KEY)
    PROJECT = RF.workspace().project(PROJECT_ID)
    VERSION = PROJECT.version(VERSION_NUMBER)

    print("Finished Loading Environment.\n")

def main():
    print("Starting analysis")

    environment_load()
    print_parameters()



if __name__ == '__main__':
    main()