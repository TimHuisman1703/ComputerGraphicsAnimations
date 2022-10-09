from imports import render_video, DIRECTORY
import os

HIGH_QUALITY = True

BLACKLIST = [
    "camera_projection_scene.py",
]

for filename in sorted(os.listdir(DIRECTORY)):
    if filename.endswith("_scene.py") and filename not in BLACKLIST:
        render_video(f"{DIRECTORY}\\{filename}", HIGH_QUALITY)