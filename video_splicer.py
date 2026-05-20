import cv2
import os

print("Target Separator: Using an aim training application, will" \
        " determine the target and crosshair being used in order to" \
        " correctly track movements from the mouse corresponding to target" \
        " for different scenarios.\n")

video_path = input(("Enter relevant video path:"))
spliced_videos = "raw_dataset"

print(f"Spliced videos will put into the {spliced_videos} directory")
os.makedirs(spliced_videos, exist_ok=True)
cap = cv2.VideoCapture(video_path)

frame_count = 0
saved_count = 0

print("Now splicing specified video:")
while cap.isOpened():
    successful_read, frame = cap.read()

    # check if frame was correctly collected
    if not successful_read:
        print("Video has ended, or frame read unsuccessful")    
        break

    # collect splices at every 30th frame
    if frame_count % 30 == 0:
        img_name = f"{video_path}_frame_{saved_count:04d}.jpg"
        out_path = os.path.join(spliced_videos, img_name)

        cv2.imwrite(out_path, frame)
        saved_count += 1
    
    frame_count += 1

cap.release()
print(f"Video splicing complete. Saved {saved_count} frames to {out_path}")    
