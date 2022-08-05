from manimlib import *
from math import pi, sqrt, sin, cos
import numpy as np
import os

DIRECTORY = os.path.realpath(os.path.dirname(__file__))

class CGScene(Scene):
    def get_title(self):
        return "Untitled"

    def all_objects(self):
        return Group(*filter(lambda x: issubclass(type(x), Mobject), self.mobjects)).remove(self.background, self.title_text)

    def construct(self):
        # Background
        self.background_color = "#36393F"
        self.background = Rectangle(15, 10, color=self.background_color, fill_opacity=1)
        self.add(self.background)

        # Title
        self.title_text = Text(self.get_title())
        self.title_text.scale(2)
        self.add(self.title_text)

        # Move title
        self.title_text.generate_target()
        self.title_text.target.set_fill("#FFFFFF", 0.5)
        self.title_text.target.scale(0.3)
        self.title_text.target.to_corner(LEFT + UP)
        self.play(
            MoveToTarget(self.title_text),
            run_time = 0.4
        )

        self.animate()

        self.wait(3)

    def animate(self):
        pass

class ReflectionRayScene(CGScene):
    def get_title(self):
        return "Reflection Ray Formula"

    def animate(self):
        # Creation

        # Mirror group
        mirror_group = Group()
        mirror_line = Line(LEFT * 5, RIGHT * 5, color="#FFFFFF")
        mirror_text = Text("Mirror", color="#FFFFFF").move_to(0.3 * UP + 4 * LEFT).scale(0.75)
        mirror_group.add(mirror_line, mirror_text)
        iterations = 15
        for i in range(iterations):
            x = (i - iterations // 2) * 0.65
            diagonal_line = Line(RIGHT * x + LEFT * 0.1 + DOWN * 0.2, RIGHT * x + RIGHT * 0.1)
            mirror_group.add(diagonal_line)

        # Normal group
        normal_group = Group()
        normal_arrow = Arrow().put_start_and_end_on((0, 0, 0), UP * 4).set_color("#FF7F00")
        normal_text = Tex("\hat{N}", color="#FF7F00").move_to(LEFT * 0.3 + UP * 3.5)
        normal_group.add(normal_arrow, normal_text)

        # Light group
        light_group = Group()
        light_arrow = Arrow().put_start_and_end_on((0, 0, 0), LEFT * sqrt(12) + UP * 2).set_color("#FFFF00")
        light_text = Tex("\hat{L}", color="#FFFF00").move_to(LEFT * sqrt(12) + UP * 1.6)
        light_group.add(light_arrow, light_text)
        sun_image = ImageMobject(f"{DIRECTORY}/assets/sun.png").scale(0.2).move_to(LEFT * sqrt(12) * 1.25 + UP * 2.5)

        # Reflection group
        reflection_group = Group()
        reflection_arrow = Arrow().put_start_and_end_on((0, 0, 0), RIGHT * sqrt(12) + UP * 2).set_color("#FF007F")
        reflection_text = Tex("R", color="#FF007F").move_to(RIGHT * (sqrt(12) - 0.5) + UP * 2.1)
        reflection_group.add(reflection_arrow, reflection_text)

        # Negative light arrow
        negative_light_arrow = light_arrow.copy().set_color("#FFFF00")
        negative_light_text = Tex("-\hat{L}", color="#FFFF00").move_to(RIGHT * 3.5 + DOWN * 2.2)
        negative_light_text

        # Dotted line
        dotted_line = DashedLine(light_arrow.get_end(), (0, light_arrow.get_end()[1]), dash_length=0.2)
        angle = 5 * pi / 6
        angle_arc = Arc(radius=0.5, start_angle=angle, angle=0.5 * pi - angle)

        # Small normal A
        small_normal_arrow_a = Arrow().put_start_and_end_on((0, 0, 0), UP * 4).set_color("#FF3F00")
        small_normal_text_a = Tex("\cos(\\angle(\hat{L}, \hat{N})) \cdot \hat{N}", color="#FF3F00").move_to(RIGHT * 1.3 + UP * 2).scale(0.6)

        # Formula group
        formula_texts = [
            Tex("R", color="#FF007F"),
            Tex("="),
            Tex("-\hat{L}", color="#FFFF00"),
            Tex("+"),
            Tex("2 \cdot \cos(\\angle(\hat{L}, \hat{N})) \cdot \hat{N}", color="#FF3F00"),
        ]
        new_formula_text = Tex("2 \cdot \mathrm{dot}(\hat{L}, \hat{N}) \cdot \hat{N}", color="#FF3F00")
        question_mark_text = Tex("?", color="#7F7F7F")

        formula_texts[0].move_to(LEFT * 5.5 + DOWN * 2)
        for i in range(1, len(formula_texts)):
            formula_texts[i].next_to(formula_texts[i - 1], RIGHT)
        formula_group = Group(*formula_texts)
        new_formula_text.next_to(formula_texts[-2], RIGHT).shift((0, 0.5, 0))
        question_mark_text.next_to(formula_texts[1], RIGHT)

        dot_formula_text = Tex("\cos(\\angle(\hat{L}, \hat{N})) = \\frac{\mathrm{dot}(\hat{L}, \hat{N})}{|\hat{L}| \cdot |\hat{N}|} = \\frac{\mathrm{dot}(\hat{L}, \hat{N})}{1 \cdot 1} = \mathrm{dot}(\hat{L}, \hat{N})")
        dot_formula_text.scale(0.8).shift(LEFT * 2.4 + DOWN * 2.2)

        explanation_text_a = Text("This formula works if L is defined as pointing\nfrom surface to light source.").scale(0.8).move_to(RIGHT + UP * 1.8)
        explanation_text_b = Text("If L is defined as pointing from light source\nto surface, the formula is negated:").scale(0.8).move_to(RIGHT + DOWN * 0.8)
        
        negative_formula_texts = [
            Tex("R", color="#FF007F"),
            Tex("="),
            Tex("\hat{L}", color="#FFFF00"),
            Tex("+"),
            Tex("-2 \cdot \mathrm{dot}(\hat{L}, \hat{N}) \cdot \hat{N}", color="#FF3F00"),
        ]
        for i in range(1, len(negative_formula_texts)):
            negative_formula_texts[i].next_to(negative_formula_texts[i - 1], RIGHT)
        negative_formula_group = Group(*negative_formula_texts)
        negative_formula_group.scale(0.8).move_to(RIGHT + DOWN * 1.8)

        # Animation

        self.play(
            FadeIn(mirror_group),
            FadeIn(normal_group),
            FadeIn(sun_image),
            run_time=1
        )

        light_group.shift((-sqrt(3) * 5, 5, 0))
        self.play(
            light_group.animate.shift((sqrt(3) * 5, -5, 0)),
            run_time=1
        )

        self.play(
            ShowCreation(reflection_arrow),
            FadeIn(reflection_text),
            run_time=1
        )

        self.wait(1)

        self.play(
            TransformMatchingTex(reflection_text.copy(), formula_texts[0]),
            FadeIn(formula_texts[1]),
            FadeIn(question_mark_text),
        )

        self.wait(1)

        self.play(
            negative_light_arrow.animate.put_start_and_end_on((0, 0, 0), RIGHT * sqrt(12) + DOWN * 2),
            TransformMatchingTex(light_text.copy(), negative_light_text),
        )

        self.wait(1)

        self.play(
            ShowCreation(dotted_line),
            ShowCreation(angle_arc),
            run_time=0.6
        )

        self.wait(1)

        self.play(
            small_normal_arrow_a.animate.put_start_and_end_on(LEFT - LEFT, (0, light_arrow.get_end()[1], 0)),
            TransformMatchingTex(normal_text.copy(), small_normal_text_a),
        )
        self.add(small_normal_arrow_a.copy())

        self.wait(1)

        self.play(
            small_normal_arrow_a.animate.shift(negative_light_arrow.get_end()),
            small_normal_text_a.animate.shift(negative_light_arrow.get_end() + DOWN * 0.4),
            run_time = 0.6
        )

        small_normal_arrow_b = small_normal_arrow_a.copy()
        small_normal_text_b = small_normal_text_a.copy()

        self.play(
            small_normal_arrow_b.animate.shift((0, -negative_light_arrow.get_end()[1], 0)),
            small_normal_text_b.animate.shift((0, -negative_light_arrow.get_end()[1], 0)),
            run_time = 0.6
        )

        self.wait(1)

        self.play(
            FadeOut(question_mark_text, DOWN),
            TransformMatchingTex(negative_light_text.copy(), formula_texts[2]),
            FadeIn(formula_texts[3]),
            TransformMatchingTex(small_normal_text_a.copy(), formula_texts[4]),
            TransformMatchingTex(small_normal_text_b.copy(), formula_texts[4]),
        )

        self.wait(2)

        formula_group.generate_target()
        formula_group.target.scale(0.6)
        formula_group.target.shift((0, 1, 0))

        self.play(
            MoveToTarget(formula_group),
        )
        self.play(
            Write(dot_formula_text),
            run_time = 1.2
        )

        self.wait(2.5)

        formula_group.target.shift((0, -0.5, 0))
        formula_group.target.scale(1 / 0.6)
        dot_formula_text.generate_target()
        dot_formula_text.target.shift((0, -0.75, 0)),
        dot_formula_text.target.set_color("#7F7F7F")
        self.play(
            MoveToTarget(formula_group),
            MoveToTarget(dot_formula_text)
        )
        self.play(
            TransformMatchingTex(formula_texts[-1], new_formula_text),
        )

        self.wait(3)

        formula_group.remove(formula_texts[-1])
        formula_group.add(new_formula_text)
        formula_group.generate_target()
        formula_group.target.scale(0.8)
        formula_group.target.move_to(RIGHT + UP * 0.8)
        objects_to_delete = self.all_objects().remove(formula_group, sun_image, light_group, mirror_group)
        self.play(
            FadeOut(objects_to_delete),
            FadeIn(explanation_text_a),
            MoveToTarget(formula_group),
            sun_image.animate.move_to(LEFT * 5 + UP * 2),
            light_arrow.animate.put_start_and_end_on(LEFT * 5 + DOWN * 1.5, LEFT * 5 + UP * 1.5),
            light_text.animate.move_to(LEFT * 5.3),
            mirror_group.animate.move_to(LEFT * 9 + DOWN * 1.5),
            run_time = 1.2
        )
        self.add(formula_group)

        self.wait(2)

        self.play(
            FadeIn(explanation_text_b),
            FadeIn(negative_formula_group),
            Rotate(
                light_arrow,
                pi,
                axis = np.array([0, 0, 1]),
                about_point = LEFT * 5
            ),
            run_time = 1.2
        )

class MatrixTransformationScene(CGScene):
    MATRIX_TRANSFORMATION_SETTINGS = {
        "title": "Matrix Transform Test",
        "scale": 0.6,
        "grid_range": ((-1, 10), (-3, 7)),
        "transformations": [
            {
                "operation": "translate",
                "data": [2, -sqrt(2)],
                "description": "\mathrm{Translation\,by\,}(2, -\sqrt{2})",
                "transform_matrix": [
                    ["1", "0", "2"],
                    ["0", "1", "-\sqrt{2}"],
                    ["0", "0", "1"]
                ],
                "result_matrix": [
                    ["1", "0", "2"],
                    ["0", "1", "-\sqrt{2}"],
                    ["0", "0", "1"]
                ],
            },
            {
                "operation": "rotate",
                "data": pi / 4,
                "description": "\mathrm{Rotation\,by\,}\\frac{\pi}{4}",
                "transform_matrix": [
                    ["\\frac{\sqrt{2}}{2}", "-\\frac{\sqrt{2}}{2}", "0"],
                    ["\\frac{\sqrt{2}}{2}", "\\frac{\sqrt{2}}{2}", "0"],
                    ["0", "0", "1"]
                ],
                "result_matrix": [
                    ["\\frac{\sqrt{2}}{2}", "-\\frac{\sqrt{2}}{2}", "\sqrt{2} + 1"],
                    ["\\frac{\sqrt{2}}{2}", "\\frac{\sqrt{2}}{2}", "\sqrt{2} - 1"],
                    ["0", "0", "1"]
                ],
            },
            {
                "operation": "scale",
                "data": [3, 2],
                "description": "\mathrm{Scaling\,by\,}(3, 2)",
                "transform_matrix": [
                    ["3", "0", "0"],
                    ["0", "2", "0"],
                    ["0", "0", "1"]
                ],
                "result_matrix": [
                    ["\\frac{3\sqrt{2}}{2}", "-\\frac{3\sqrt{2}}{2}", "3\sqrt{2} + 3"],
                    ["\sqrt{2}", "\sqrt{2}", "2\sqrt{2} - 2"],
                    ["0", "0", "1"]
                ],
            },
        ]
    }

    def get_title(self):
        return self.MATRIX_TRANSFORMATION_SETTINGS["title"]

    def animate(self):
        # Creation

        # Calculate center
        scale = self.MATRIX_TRANSFORMATION_SETTINGS["scale"]
        grid_range = self.MATRIX_TRANSFORMATION_SETTINGS["grid_range"]
        center = np.array([-6.5 - scale * grid_range[0][0], -0.3 - scale * sum(grid_range[1]) / 2, 0])

        # Grid group
        grid_group = Group()
        for iy in range(grid_range[1][0] + 1, grid_range[1][1]):
            if iy == 0:
                continue
            new_line = Line(center + scale * np.array([grid_range[0][0], iy, 0]), center + scale * np.array([grid_range[0][1], iy, 0]), color="#5F5F5F")
            grid_group.add(new_line)
        for ix in range(grid_range[0][0] + 1, grid_range[0][1]):
            if ix == 0:
                continue
            new_line = Line(center + scale * np.array([ix, grid_range[1][0], 0]), center + scale * np.array([ix, grid_range[1][1], 0]), color="#5F5F5F")
            grid_group.add(new_line)
        x_axis = Line(center + scale * np.array([grid_range[0][0], 0, 0]), center + scale * np.array([grid_range[0][1], 0, 0]), color="#9F9F9F")
        y_axis = Line(center + scale * np.array([0, grid_range[1][0], 0]), center + scale * np.array([0, grid_range[1][1], 0]), color="#9F9F9F")
        grid_group.add(x_axis, y_axis)

        # Object group
        object_group = Group()
        u_arrow = Arrow().put_start_and_end_on(center, center + scale * RIGHT).set_color("#FF0000")
        v_arrow = Arrow().put_start_and_end_on(center, center + scale * UP).set_color("#00FF00")
        unit_square = Square(side_length=scale).move_to(center + 0.5 * scale * (UP + RIGHT)).set_color("#FFFF00").set_opacity(0.5).set_fill("#FFFF00", opacity=0.25)
        object_group.add(unit_square, v_arrow, u_arrow)
        
        # Current matrix
        current_matrix = Matrix(
            [["1", "0", "0"], ["0", "1", "0"], ["0", "0", "1"]],
            h_buff = 1.6,
            v_buff = 1.5
        ).scale(0.6).shift(RIGHT * 5 + DOWN * 2)
        current_matrix_text = Tex("\mathrm{Current}").scale(0.5).next_to(current_matrix, UP)
        
        # List of transformations
        transformations = self.MATRIX_TRANSFORMATION_SETTINGS["transformations"]
        description_texts = [
            Tex(j["description"]).scale(0.75).set_color("#7F7F7F") for j in transformations
        ]
        description_group = Group(*description_texts)
        description_group.arrange(DOWN, buff=0.2)
        description_group.shift(RIGHT * 4 + UP * 2.5)

        # Animation

        # Fade in
        self.play(
            FadeIn(grid_group),
            FadeIn(object_group),
            FadeIn(current_matrix),
            FadeIn(current_matrix_text),
            FadeIn(description_group),
            run_time = 1
        )

        for i in range(len(transformations)):
            transformation = transformations[i]
            operation = transformation["operation"]

            # Get new matrices
            transform_matrix = Matrix(
                transformation["transform_matrix"],
                h_buff = 1.6,
                v_buff = 1.5
            ).scale(0.6).next_to(current_matrix, LEFT)
            description_text = Tex(
                transformation["description"]
            ).scale(0.5).next_to(transform_matrix, UP)
            result_matrix = Matrix(
                transformation["result_matrix"],
                h_buff = 1.6,
                v_buff = 1.5
            ).scale(0.6).move_to(current_matrix)

            self.wait(0.5)

            # Show transform matrix
            self.play(
                FadeIn(transform_matrix),
                FadeIn(description_text),
                description_texts[i].animate.set_color("#FFFF00"),
                *([description_texts[i - 1].animate.set_color("#BFBFBF")] * (i > 0)),
                run_time = 0.8
            )

            self.wait(0.5)

            # Determine transformation animations
            actions = [
                FadeOut(transform_matrix, RIGHT * 3),
                FadeOut(description_text, RIGHT * 3),
                FadeOut(current_matrix),
                FadeIn(result_matrix),
                current_matrix_text.animate.next_to(result_matrix, UP),
            ]
            if operation == "translate":
                offset = transformation["data"]
                actions.append(
                    object_group.animate.shift((scale * offset[0], scale * offset[1], 0))
                )
            elif operation == "scale":
                factor = transformation["data"]
                object_group.generate_target()
                object_group.target.stretch(
                    factor[0],
                    0,
                    about_point = center
                ),
                object_group.target.stretch(
                    factor[1],
                    1,
                    about_point = center
                )
                actions.append(
                    MoveToTarget(object_group)
                )
            elif operation == "rotate":
                angle = transformation["data"]
                actions.append(
                    Rotate(
                        object_group,
                        angle,
                        axis = np.array([0, 0, 1]),
                        about_point = center
                    )
                )

            self.play(
                *actions,
                run_time = 1
            )

            # Update current matrix
            current_matrix = result_matrix

PREVIEW = True
ANIMATION = "MatrixTransformationScene"
SKIP_TO = 0

if __name__ == "__main__":
    if PREVIEW:
        os.system(f"manimgl {DIRECTORY}/main.py {ANIMATION} -l -n {SKIP_TO}")
    else:
        os.system(f"manim-render {DIRECTORY}/main.py {ANIMATION} -w --hd --frame_rate 60")