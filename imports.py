if __name__ == "__main__":
    print("\033[0m\n\033[1;31mThis is the imports file, not a scene file.\n\033[1;36mTo render a video, run any of the files ending in \"\033[1;33m_scene.py\033[1;36m\".\n\n\033[0m", end="")
    exit()

from manim import *
import numpy as np
import os

DIRECTORY = os.path.realpath(os.path.dirname(__file__))
BACKGROUND_COLOR = "#36393F"

config.background_color = BACKGROUND_COLOR

def render_video(filename, high_quality=True, start_at=0, end_at=1000):
    command = "echo lmao"

    if not os.path.exists(f"{DIRECTORY}/videos"):
        os.mkdir(f"{DIRECTORY}/videos")

    name = filename.split("\\")[-1][:-3]
    output_filename = f"{DIRECTORY}\\videos\\{name}.mp4"

    if high_quality:
        command = f"manim {filename} MainScene --write_to_movie --output_file {output_filename} --from_animation_number {start_at},{end_at} --resolution 1920,1080 --frame_rate 60"
    else:
        command = f"manim {filename} MainScene -p --disable_caching --from_animation_number {start_at},{end_at} --resolution 480,270 --frame_rate 5"

    print(f"\033[0;32m{command}\033[0m")
    os.system(command)

class CGScene(ThreeDScene):
    def get_title(self):
        return "Untitled"

    def all_objects(self):
        return Group(*filter(lambda x: issubclass(type(x), Mobject), self.mobjects)).remove(self.title_text)

    def generate_grid(self, grid_range):
        grid_group = Group()

        # Place horizontal grid lines
        for iy in range(grid_range[1][0] + 1, grid_range[1][1]):
            if iy == 0:
                continue
            new_line = Line(np.array([grid_range[0][0], iy, 0]), np.array([grid_range[0][1], iy, 0]), color="#5F5F5F")
            grid_group.add(new_line)

        # Place vertical grid lines
        for ix in range(grid_range[0][0] + 1, grid_range[0][1]):
            if ix == 0:
                continue
            new_line = Line((ix, grid_range[1][0], 0), (ix, grid_range[1][1], 0), color="#5F5F5F")
            grid_group.add(new_line)

        # Place axes
        x_axis = Line(np.array([grid_range[0][0], 0, 0]), np.array([grid_range[0][1], 0, 0]), color="#9F9F9F")
        y_axis = Line(np.array([0, grid_range[1][0], 0]), np.array([0, grid_range[1][1], 0]), color="#9F9F9F")
        grid_group.add(x_axis, y_axis)

        return grid_group

    def generate_crosshairs(self):
        # Place arrows
        u_arrow = Arrow().set_color("#FF0000").put_start_and_end_on(ORIGIN, RIGHT)
        v_arrow = Arrow().set_color("#00FF00").put_start_and_end_on(ORIGIN, UP)

        # Place unit square
        unit_square = Square(side_length=1.0).move_to((0.5, 0.5, 0)).set_color("#FFFF00").set_opacity(0.5).set_fill("#FFFF00", opacity=0.25)

        return Group(unit_square, v_arrow, u_arrow)

    def get_animation_number(self):
        return self.num_plays

    def swap_caption(self, text, **kwargs):
        # Set default kwargs
        t2c = kwargs.get("t2c", {})
        t2s = kwargs.get("t2s", {})
        scale = kwargs.get("scale", 0.7)
        pos = kwargs.get("pos", DOWN * 2.8)

        # Group text in new lines
        texts = text.split()
        final_text = ""
        line_length = 0
        for t in texts:
            if line_length + 1 + len(t) <= 60:
                final_text += " " + t
                line_length += 1 + len(t)
            else:
                final_text += "\n" + t
                line_length = len(t)
        final_text = final_text[1:]

        # Print current text
        print("\033[1;34m", end="")
        final_text_lines = final_text.split("\n")
        for i in range(len(final_text_lines)):
            print(["  ", "\n- "][i == 0] + final_text_lines[i])
        print("\033[0m", end="")

        # Create new caption
        new_caption = Text(final_text, t2s=t2s).set_color("#FFFFFF")
        new_caption.scale(scale).shift(pos)
        new_caption._set_color_by_t2c(t2c)
        new_caption.z_index = 100
        new_caption.add_background_rectangle("#000000", 0.5, buff=0.2, corner_radius=0.2)
        self.add_fixed_in_frame_mobjects(new_caption)
        actions = [FadeIn(new_caption, shift=UP)]

        # Delete old caption
        if self.caption:
            actions.extend([FadeOut(self.caption)])

        self.caption = new_caption
        return actions
    
    def get_asset(self, filename):
        return f"{DIRECTORY}/assets/{filename}"

    def appear(self, obj):
        if type(obj) == Arrow:
            start = obj.get_start()
            end = obj.get_end()

            obj.generate_target()
            obj.put_start_and_end_on(start, start + 0.001 * (end - start))
            obj.set_fill(opacity=0).set_stroke(opacity=0)
            return MoveToTarget(obj)
        else:
            return Create(obj)
    
    def disappear(self, obj):
        if type(obj) == Arrow:
            start = obj.get_start()
            end = obj.get_end()

            obj.generate_target()
            obj.target.put_start_and_end_on(end + 0.001 * (start - end), end)
            obj.target.set_fill(opacity=0).set_stroke(opacity=0)
            return MoveToTarget(obj)
        else:
            return Uncreate(obj)

    def construct(self):
        # Title
        self.title_text = Text(self.get_title()).set_color("#FFFFFF")
        self.title_text.generate_target()
        self.title_text.set_width(13)
        self.add(self.title_text)
        self.wait(1.5)

        # Move title to corner
        self.title_text.target.set_fill("#FFFFFF", 0.5)
        self.title_text.target.scale(0.6)
        self.title_text.target.to_corner(LEFT + UP)
        self.play(
            MoveToTarget(self.title_text),
            run_time = 0.4
        )
        self.add_fixed_in_frame_mobjects(self.title_text)

        # Default values
        self.caption = None

        # Run animation
        self.animate()

        # Ending pause
        print()
        self.wait(3)

    def animate(self):
        pass