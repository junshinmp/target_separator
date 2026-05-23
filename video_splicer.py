import cv2
import os
import time

from pathlib import Path

print("Target Separator: Using an aim training application, will" \
        " determine the target and crosshair being used in order to" \
        " correctly track movements from the mouse corresponding to target" \
        " for different scenarios.")

data_dir = Path("training_data")
spliced_videos = Path("raw_dataset")
FRAME_SPLICE = 60

# tracking variables for statistical info
total_result_frames = 0
total_time = 0
times_per_split = {}
frame_count = 0
saved_count = 0
out_path = ""

print(f"Spliced videos will be put into the {spliced_videos} directory")
os.makedirs(spliced_videos, exist_ok=True)

existing_images = []
for video_dir in spliced_videos.iterdir():
    if video_dir.is_dir():
        existing_images.append(video_dir.name)

for file_path in data_dir.iterdir():
    print("\n---------------------------------------\n")
    start_time = time.perf_counter()
    if not file_path.is_file() or file_path.suffix.lower() not in [".mp4", ".avi", ".mkv", ".mov"]:
        continue

    video_dir_name = f"{file_path.stem}_dir"
    video_output_path = os.path.join(spliced_videos, video_dir_name)
    os.makedirs(video_output_path, exist_ok=True)

    if video_dir_name in existing_images:
        print(f"{video_dir_name} already exists in {spliced_videos}, skipping.")
        continue

    cap = cv2.VideoCapture(str(file_path))

    frame_count = 0
    saved_count = 0
    out_path = ""

    print(f"Now splicing specified video: {file_path.stem}")
    while cap.isOpened():
        successful_read, frame = cap.read()

        # check if frame was correctly collected
        if not successful_read:
            print("Video has ended, or frame read unsuccessful")    
            break

        # collect splices at every 30th frame
        if frame_count % FRAME_SPLICE == 0:
            img_name = f"{file_path.stem}_frame_{saved_count:04d}.jpg"
            out_path = os.path.join(video_output_path, img_name)

            cv2.imwrite(out_path, frame)
            saved_count += 1
        
        frame_count += 1
        total_result_frames += 1

    cap.release()

    # stats calc
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    times_per_split[file_path.stem] = elapsed_time
    total_time += elapsed_time


    print(f"Video splicing for {file_path.stem} complete. Saved {saved_count} frames to {out_path}\n")

print("\n---------------------------------------\n")
print("Completed splicing all videos in training data directory.")
print("Statistics:")
print(f"Total Spliced Frames: {frame_count}")
print(f"Total Elapsed Time: {total_time:.2f}")

for key, val in times_per_split.items():
    print(f" - {key}: {val:.2f} seconds")

print("\n---------------------------------------\n")
