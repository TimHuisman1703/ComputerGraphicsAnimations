from imports import render_video, DIRECTORY

HIGH_QUALITY = True

LIST = [
    "alpha_blending_scene.py",
    "bilinear_interpolation_scene.py",
    "camera_projection_scene.py",
    "matrix_reading_order_scene.py",
    "reflection_ray_scene.py",
]

for filename in LIST:
    render_video(f"{DIRECTORY}\\{filename}", HIGH_QUALITY, 0, 1000)