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