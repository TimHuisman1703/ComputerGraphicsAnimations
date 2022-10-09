from imports import *
from manim import *
from math import cos, pi, sin, sqrt

class MainScene(CGScene):
    def get_title(self):
        return "Template Scene"

    def animate(self):
        # Write your code in this function
        text = Text("Your video here!")
        self.play(
            Write(text)
        )

HIGH_QUALITY = False
START_AT = 0
END_AT = 1000

if __name__ == "__main__":
    render_video(os.path.realpath(__file__), HIGH_QUALITY, START_AT, END_AT)