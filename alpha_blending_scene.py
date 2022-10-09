from imports import *
from manim import *
from math import pi

class MainScene(CGScene):
    def get_title(self):
        return "Alpha Blending"

    def animate(self):
        # Show scene
        self.black_background = RoundedRectangle(width=4, height=4, corner_radius=0.5, stroke_opacity=0, fill_opacity=1).shift(UP * 1.5).set_fill("#000000")
        alpha_slider_line = Line(LEFT * 4 + DOWN * 1.35, RIGHT * 4 + DOWN * 1.35, stroke_width=4, color="#BFBFBF")
        alpha_slider_text = Text("alpha").scale(0.8).next_to(alpha_slider_line, UP, buff=0.1)
        self.alpha_slider_triangle = Triangle(color="#FFFFFF", fill_opacity=1).move_to(DOWN * 1.6).scale(0.2)
        alpha_slider_text_zero = Text("0.0", color="#BFBFBF").scale(0.6).next_to(alpha_slider_line, LEFT)
        alpha_slider_text_one = Text("1.0", color="#BFBFBF").scale(0.6).next_to(alpha_slider_line, RIGHT)
        alpha_slider_group = Group(alpha_slider_line, alpha_slider_text, self.alpha_slider_triangle, alpha_slider_text_zero, alpha_slider_text_one)
        red_square = Square(side_length=2, color="#FF0000", stroke_opacity=0, fill_opacity=1).move_to(self.black_background).shift(0.5 * LEFT + 0.5 * UP)
        self.blue_square = Square(side_length=2, color="#007FFF", stroke_opacity=0, fill_opacity=0.5).move_to(self.black_background).shift(0.5 * RIGHT + 0.5 * DOWN)
        square_group = Group(red_square, self.blue_square)
        self.play(
            FadeIn(self.black_background),
            FadeIn(alpha_slider_group),
            FadeIn(square_group)
        )
        self.wait(1)

        self.play(
            *self.swap_caption("Transparency of a color is handled by assigning an \"alpha\" value to it, which indicates the opacity of the color.")
        )
        self.wait(3.5)

        self.play(
            *self.swap_caption("When multiple objects overlap in front of the camera, their alpha values are used to determine the resulting color.")
        )
        self.wait(1)

        # Function for moving alpha slider
        def set_alpha_slider(alpha):
            return [
                self.alpha_slider_triangle.animate.move_to(RIGHT * (8 * alpha - 4) + DOWN * 1.6),
                self.blue_square.animate.set_fill(opacity=alpha)
            ]

        # Set alpha to 0.2
        self.play(
            *set_alpha_slider(0.2),
            run_time = 1.5
        )
        self.wait(0.5)

        # Set alpha to 0.7
        self.play(
            *set_alpha_slider(0.7),
            run_time = 1.5
        )
        self.wait(1.5)

        # Set alpha to 0.0
        self.play(
            *set_alpha_slider(0.0),
            *self.swap_caption("An alpha of 0.0 means the color is completely invisible."),
            run_time = 1.5
        )
        self.wait(3)

        # Set alpha to 1.0
        self.play(
            *set_alpha_slider(1.0),
            *self.swap_caption("An alpha of 1.0 means the color is opaque and not transparent at all."),
            run_time = 1.5
        )
        self.wait(3)

        # Show second scene
        self.bar_parts_rectangle = Rectangle("#BFBFBF", 4, 1, fill_opacity=1).set_fill("#000000").shift(RIGHT * 2 + 0.5 * UP)
        self.bar_blend_rectangle = Rectangle("#BFBFBF", 4, 1, fill_opacity=1).set_fill("#000000").shift(RIGHT * 0.5 + 0.5 * UP)
        bar_blend_text = Text("Mix", color="#BFBFBF").scale(0.5).next_to(self.bar_blend_rectangle, UP)
        bar_group = Group(
            self.bar_parts_rectangle,
            self.bar_blend_rectangle,
            bar_blend_text
        )
        x = self.bar_parts_rectangle.get_center()[0]
        for iy in range(0, 11):
            new_line_left = Line(RIGHT * (x - 0.6) + UP * (0.4 * iy - 1.5), RIGHT * (x - 0.5) + UP * (0.4 * iy - 1.5), color="#BFBFBF")
            new_line_right = Line(RIGHT * (x + 0.5) + UP * (0.4 * iy - 1.5), RIGHT * (x + 0.6) + UP * (0.4 * iy - 1.5), color="#BFBFBF")
            bar_group.add(new_line_left, new_line_right)
        formula_black_square = Square(side_length=0.32, color="#BFBFBF", fill_opacity=1).set_fill("#000000")
        self.formula_text = Text("Color = ", color="#BFBFBF").scale(0.5).to_corner(LEFT + DOWN).shift(RIGHT * 2.2 + UP * 1.5)
        self.formula_group = Group(formula_black_square).next_to(self.formula_text, RIGHT, buff=0.2)
        self.play(
            FadeOut(alpha_slider_group),
            FadeOut(square_group),
            self.black_background.animate.shift(3.5 * LEFT + DOWN),
            FadeIn(bar_group),
            FadeIn(self.formula_text),
            FadeIn(self.formula_group),
            *self.swap_caption("With multiple overlaps, alpha blending works like this.", pos=DOWN * 3),
            run_time = 1
        )
        self.wait(1)

        # Function for inserting new alpha
        self.red = self.green = self.blue = 0.0
        self.rectangle_group = Group(
            Rectangle("#BFBFBF", 4, 1, fill_opacity=1).set_fill("#000000").move_to(self.bar_parts_rectangle)
        )
        self.green_contributes_group = Group()
        def add_alpha_bar(alpha, color, circle_pos, iteration):
            # Create rectangle and circle
            rectangle = Rectangle("#BFBFBF", 4 * alpha, 1, fill_opacity=1).set_fill(color).move_to(self.bar_parts_rectangle).shift(2.5 * RIGHT + 2 * (1.0 - alpha) * DOWN)
            circle = Circle(radius=1.2, color=color, stroke_opacity=alpha, fill_opacity=0).move_to(self.black_background.get_center() + circle_pos).set_fill(color)
            color_text = Text(f"alpha = {alpha}").scale(0.6).next_to(rectangle, UP)
            self.play(
                Create(circle),
                FadeIn(rectangle),
                FadeIn(color_text)
            )
            self.wait(0.5)

            if iteration == 0:
                self.wait(0.5)

                self.play(
                    *self.swap_caption("When overlapping with a new color, the old color should first be scaled to make room for the new color.", pos=DOWN * 3)
                )
                self.wait(1)

            # Scale other rectangles
            self.red *= (1.0 - alpha)
            self.green *= (1.0 - alpha)
            self.blue *= (1.0 - alpha)
            brace = Brace(self.rectangle_group, RIGHT)
            self.rectangle_group.add(brace)
            self.rectangle_group.generate_target()
            self.rectangle_group.target.stretch(1.0 - alpha, 1)
            self.rectangle_group.target.shift(alpha * 2 * UP)

            formula_actions = []
            if iteration > 0:
                parenthesis_left = Tex("$($").scale(0.6 + iteration * 0.15).next_to(self.formula_group, LEFT, buff=0.1)
                parenthesis_right = Tex("$)$").scale(0.6 + iteration * 0.15).next_to(self.formula_group, RIGHT, buff=0.1)
                self.formula_group.add(parenthesis_left, parenthesis_right)
                formula_actions.extend([
                    FadeIn(parenthesis_left),
                    FadeIn(parenthesis_right),
                    self.formula_text.animate.next_to(self.formula_group, LEFT, buff=0.2)
                ])

            self.play(
                *formula_actions,
                FadeIn(brace),
                run_time = 0.6
            )
            formula_text_a = Tex(f"$\cdot \, {1.0 - alpha:.1}$").scale(0.6).next_to(self.formula_group, RIGHT, buff=0.1)
            self.formula_group.add(formula_text_a)
            if iteration > 1:
                self.green_contributes_group.add(formula_text_a)
            self.play(
                self.bar_blend_rectangle.animate.set_fill(rgb_to_color((self.red, self.green, self.blue)), opacity=1),
                MoveToTarget(self.rectangle_group),
                FadeIn(formula_text_a, shift=LEFT),
                run_time = 0.8
            )

            # Remove brace from rectangle group
            self.rectangle_group.remove(brace)
            self.add(brace)

            if iteration == 0:
                self.wait(2)

                self.play(
                    *self.swap_caption("Once room has been made, the new color, multiplied by its alpha value, is added to the final color.", pos=DOWN * 3)
                )
                self.wait(1)

            # Insert new rectangle
            self.red += alpha * int(color[1:3], 16) / 255
            self.green += alpha * int(color[3:5], 16) / 255
            self.blue += alpha * int(color[5:7], 16) / 255
            circle.generate_target()
            circle.target.set_fill(color, opacity=alpha)
            circle.target.set_stroke(color, opacity=0)
            formula_text_b = Tex("$+$").scale(0.6).next_to(self.formula_group, RIGHT, buff=0.1)
            formula_square = Square(side_length=0.32, color="#BFBFBF", fill_opacity=1).set_fill(color).next_to(formula_text_b, RIGHT, buff=0.1)
            formula_text_c = Tex(f"$\cdot \, {alpha:.2}$").scale(0.6).next_to(formula_square, RIGHT, buff=0.1)
            if iteration == 1:
                self.green_contributes_group.add(formula_text_c)
            self.formula_group.add(formula_text_b, formula_square, formula_text_c)
            self.play(
                FadeOut(brace),
                self.bar_blend_rectangle.animate.set_fill(rgb_to_color((self.red, self.green, self.blue)), opacity=1),
                rectangle.animate.shift(2.5 * LEFT),
                FadeOut(color_text),
                MoveToTarget(circle),
                FadeIn(formula_text_b, shift=LEFT),
                FadeIn(formula_square, shift=LEFT),
                FadeIn(formula_text_c, shift=LEFT),
                run_time = 0.8
            )
            self.wait(1.5)

            if iteration == 0:
                self.play(
                    *self.swap_caption("With an alpha of 0.8, the resulting color is 80% the new\ncolor and 20% the old color.", pos=DOWN * 3)
                )
                self.wait(4)

            self.rectangle_group.add(rectangle)

        # Add red alpha bar
        add_alpha_bar(0.8, "#FF0000", LEFT * 0.5, 0)
        self.play(
            *self.swap_caption("This process is repeated when other colors overlap as well.", pos=DOWN * 3)
        )
        self.wait(0.5)

        # Add other alpha bars
        add_alpha_bar(0.4, "#00FF00", RIGHT * 0.5, 1)
        add_alpha_bar(0.5, "#007FFF", UP * 0.5, 2)
        add_alpha_bar(0.3, "#FF00FF", DOWN * 0.5, 3)

        left_center = self.black_background.get_center()
        right_center = self.bar_blend_rectangle.get_center()
        center_center = (left_center + right_center) / 2
        final_color = rgb_to_color((self.red, self.green, self.blue))

        # Add connecting rectangle for comparison
        connecting_rectangle = Rectangle("#FFFFFF", 0.4, 0.01, stroke_opacity=0, fill_opacity=1).move_to(center_center).set_fill(final_color)
        upper_line = Line(center_center + 0.005 * LEFT + UP * 0.2, center_center + 0.005 * RIGHT + UP * 0.2, color="#BFBFBF")
        lower_line = Line(center_center + 0.005 * LEFT + DOWN * 0.2, center_center + 0.005 * RIGHT + DOWN * 0.2, color="#BFBFBF")
        connecting_group = Group(
            connecting_rectangle,
            upper_line,
            lower_line
        )
        self.play(
            *self.swap_caption("Each color contributes a little to the final result.", pos=DOWN * 3),
            connecting_group.animate.stretch_to_fit_width(right_center[0] - left_center[0] - 0.6)
        )
        self.wait(3)

        self.play(
            *self.swap_caption("How much a color contributes can be calculated by observing this formula.", pos=DOWN * 3)
        )
        self.play(
            self.formula_group.animate.scale(1.1),
            run_time=0.8
        )
        self.play(
            self.formula_group.animate.scale(1 / 1.1),
            run_time=0.8
        )
        self.wait(1.4)

        # Highlight green-multiplied values, show green brace
        for j in self.green_contributes_group:
            j.generate_target()
            j.target.scale(1.2)
            j.target.set_color("#FFFF00")
        brace = Brace(self.rectangle_group[2], RIGHT)
        brace_text = Text("0.14").scale(0.6).next_to(brace, RIGHT)
        brace_group = Group(brace, brace_text)
        self.play(
            *self.swap_caption("For example, green contributes 0.4 * 0.5 * 0.7 = 14% to the final color.", pos=DOWN * 3, t2c={"green": "#00FF00", "0.4 * 0.5 * 0.7": "#FFFF00", "14%": "#FFFF00"}),
            *[MoveToTarget(j) for j in self.green_contributes_group],
            FadeIn(brace_group)
        )
        self.wait(5)

        # Red-magenta comparison
        for j in self.green_contributes_group:
            j.generate_target()
            j.target.scale(1 / 1.2)
            j.target.set_color("#FFFFFF")
        self.play(
            *self.swap_caption("Note that the order of the colors matters for the end result.", pos=DOWN * 3),
            *[MoveToTarget(j) for j in self.green_contributes_group],
            FadeOut(brace_group)
        )
        self.wait(3)

        self.play(
            *self.swap_caption("For example, even though red had a higher alpha than magenta (0.8 > 0.3), it has less influence because it is further in the back.", pos=DOWN * 3, t2c={"red": "#FF0000", "magenta": "#FF00FF", "0.8": "#FF0000", "0.3": "#FF00FF"})
        )
        self.wait(3)

HIGH_QUALITY = False
START_AT = 0
END_AT = 1000

if __name__ == "__main__":
    render_video(os.path.realpath(__file__), HIGH_QUALITY, START_AT, END_AT)