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

    def generate_grid(self, grid_range):
        grid_group = Group()

        for iy in range(grid_range[1][0] + 1, grid_range[1][1]):
            if iy == 0:
                continue
            new_line = Line(np.array([grid_range[0][0], iy, 0]), np.array([grid_range[0][1], iy, 0]), color="#5F5F5F")
            grid_group.add(new_line)

        for ix in range(grid_range[0][0] + 1, grid_range[0][1]):
            if ix == 0:
                continue
            new_line = Line((ix, grid_range[1][0], 0), (ix, grid_range[1][1], 0), color="#5F5F5F")
            grid_group.add(new_line)

        x_axis = Line(np.array([grid_range[0][0], 0, 0]), np.array([grid_range[0][1], 0, 0]), color="#9F9F9F")
        y_axis = Line(np.array([0, grid_range[1][0], 0]), np.array([0, grid_range[1][1], 0]), color="#9F9F9F")
        grid_group.add(x_axis, y_axis)

        return grid_group

    def generate_crosshairs(self):
        u_arrow = Arrow().put_start_and_end_on(ORIGIN, RIGHT).set_color("#FF0000")
        v_arrow = Arrow().put_start_and_end_on(ORIGIN, UP).set_color("#00FF00")
        unit_square = Square(side_length=1.0).move_to((0.5, 0.5, 0)).set_color("#FFFF00").set_opacity(0.5).set_fill("#FFFF00", opacity=0.25)
        return Group(unit_square, v_arrow, u_arrow)
    
    def swap_caption(self, text, **kwargs):
        t2c = kwargs.get("t2c", {})
        scale = kwargs.get("scale", 0.8)
        color = kwargs.get("color", "#FFFFFF")
        pos = kwargs.get("pos", DOWN * 2.6)
        new_caption = Text(text, t2c=t2c, color=color).scale(scale).shift(pos)
        actions = [FadeIn(new_caption, UP)]
        if self.caption:
            actions.append(FadeOut(self.caption))
        self.caption = new_caption
        return actions

    def construct(self):
        # Background
        self.background_color = "#36393F"
        self.background = Rectangle(15, 10, color=self.background_color, fill_opacity=1)
        self.add(self.background)

        # Title
        self.title_text = Text(self.get_title())
        self.title_text.generate_target()
        self.title_text.set_width(13)
        self.add(self.title_text)
        self.title_text.target.set_fill("#FFFFFF", 0.5)
        self.title_text.target.scale(0.6)
        self.title_text.target.to_corner(LEFT + UP)
        self.play(
            MoveToTarget(self.title_text),
            run_time = 0.4
        )

        # Default values
        self.caption = None

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
        grid_group = self.generate_grid(grid_range).scale(scale, about_point=ORIGIN).shift(center)

        # Object group
        object_group = self.generate_crosshairs()
        object_group.scale(scale, about_point=ORIGIN).shift(center)

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

class MatrixOrderScene(CGScene):
    def get_title(self):
        return "Right-To-Left or Left-To-Right?"

    def animate(self):
        matrices = [
            Matrix(
                [["\cos(\pi / 4)", "-\sin(\pi / 4)", "0"], ["\sin(\pi / 4)", "\cos(\pi / 4)", "0"], ["0", "0", "1"]],
                h_buff = 2.2
            ),
            Matrix(
                [["1", "0", "2"], ["0", "1", "1"], ["0", "0", "1"]],
                h_buff = 0.8
            ),
            Matrix(
                [["0.5", "0", "0"], ["0", "0.5", "0"], ["0", "0", "1"]],
                h_buff = 0.8
            ),
        ]
        matrix_descriptions_texts = [
            Text("Rotate by π/4"),
            Text("Translate by (2, 1)"),
            Text("Scale by 0.5"),
        ]
        matrix_group = Group(*matrices)
        matrix_group.arrange(RIGHT)

        for i in range(len(matrix_descriptions_texts)):
            matrix_descriptions_texts[i].scale(0.6).next_to(matrices[i], UP).set_color("#BFBFBF")
        matrix_group.add(*matrix_descriptions_texts)
        matrix_group.scale(0.9).move_to(UP)

        self.play(
            FadeIn(matrix_group)
        )

        explanation_text_a = Text("Suppose we have a few operations strung together by multiplying their matrices.").scale(0.8).move_to(DOWN * 1.5)
        self.play(
            FadeIn(explanation_text_a, UP)
        )
        self.wait(4)

        matrix_group.generate_target()
        matrix_group.target.scale(0.75)
        matrix_group.target.shift(RIGHT * 2.5 + UP * 0.5)

        scale = 0.7
        center = np.array([-6, -1, 0])
        grid_group = self.generate_grid(((-1, 5), (-1, 5))).scale(scale, about_point=ORIGIN).shift(center)
        object_group = self.generate_crosshairs().scale(scale, about_point=ORIGIN).shift(center)
        right_to_left_arrow = Arrow((6.7, 0.3, 0), (-1.7, 0.3, 0)).set_color("#00BFFF")
        left_to_right_arrow = Arrow((-1.7, 0, 0), (6.7, 0, 0)).set_color("#FF7F00")
        explanation_text_b = Text(
            "When applying these operations one at a time, should we read them right-to-left or left-to-right?",
            t2c={"right-to-left": "#00BFFF", "left-to-right": "#FF7F00"}
        ).scale(0.8).move_to(DOWN * 2.6)
        self.play(
            FadeOut(explanation_text_a),
            ShowCreation(right_to_left_arrow),
            ShowCreation(left_to_right_arrow),
            FadeIn(grid_group),
            FadeIn(object_group),
            FadeIn(explanation_text_b, UP),
            MoveToTarget(matrix_group)
        )
        self.wait(4)

        explanation_text_c = Text(
            "The usual way is right-to-left, as long as each operation is done from the perspective of the origin.",
            t2c={"right-to-left": "#00BFFF", "perspective of the origin": "#FFFF00"}
        ).scale(0.8).move_to(DOWN * 2.6)
        self.play(
            FadeOut(explanation_text_b),
            FadeOut(left_to_right_arrow),
            FadeIn(explanation_text_c, UP)
        )

        # RTL: Scale
        rtl_scale_group = Group(
            *[Circle(radius=j).set_color("#00BFFF") for j in range(4)]
        ).scale(scale, about_point=ORIGIN).shift(center)
        self.play(
            ShowCreation(rtl_scale_group),
            run_time = 1
        )
        self.wait(0.5)

        self.play(
            Indicate(matrices[2], color="#00BFFF"),
            object_group.animate.scale(
                0.5,
                about_point = center
            ),
            rtl_scale_group.animate.scale(
                0.5,
                about_point = center
            ),
            run_time = 2
        )
        self.play(
            Uncreate(rtl_scale_group),
            run_time = 1
        )

        # RTL: Translate
        rtl_translate_group = Group(
            Arrow(stroke_width=8).put_start_and_end_on(ORIGIN, RIGHT * 2).set_color("#00BFFF"),
            Arrow(stroke_width=8).put_start_and_end_on(RIGHT * 2, RIGHT * 2 + UP).set_color("#00BFFF"),
        ).scale(scale, about_point=ORIGIN).shift(center)
        self.play(
            ShowCreation(rtl_translate_group),
            run_time = 1
        )
        self.wait(0.5)

        self.play(
            Indicate(matrices[1], color="#00BFFF"),
            object_group.animate.shift((2 * scale, scale, 0)),
            run_time = 2
        )
        self.play(
            Uncreate(rtl_translate_group),
            run_time = 1
        )

        # RTL: Rotate
        rtl_rotate_group = Group(
            *[Square(2 * j).set_color("#00BFFF") for j in range(4)]
        ).scale(scale, about_point=ORIGIN).shift(center)
        self.play(
            ShowCreation(rtl_rotate_group),
            run_time = 1
        )
        self.wait(0.5)

        self.play(
            Indicate(matrices[0], color="#00BFFF"),
            Rotate(
                object_group,
                pi / 4,
                about_point = center
            ),
            Rotate(
                rtl_rotate_group,
                pi / 4,
                about_point = center
            ),
            run_time = 2
        )
        self.play(
            Uncreate(rtl_rotate_group),
            run_time = 1
        )
        self.wait(0.5)

        explanation_text_d = Text(
            "Right-to-left also makes sense in the math, since the matrix that is closest to the vector (on the right) is applied first.",
            t2c={"Right-to-left": "#00BFFF", "vector": "#FF00FF"}
        ).scale(0.8).move_to(DOWN * 2.6)
        vector_matrix = Matrix([["x"], ["y"], ["1"]]).scale(0.75).next_to(matrices[2], RIGHT).shift(LEFT * 0.6).set_color("#FF00FF")
        self.play(
            FadeOut(explanation_text_c),
            FadeIn(explanation_text_d, UP),
            matrix_group.animate.shift(LEFT * 0.5),
            FadeIn(vector_matrix, LEFT),
            run_time = 1
        )
        self.wait(4)

        new_object_group = self.generate_crosshairs().scale(scale, about_point=ORIGIN).shift(center)
        explanation_text_e = Text(
            "However, there is also a different method of applying operations, for which left-to-right reading can be used.",
            t2c={"left-to-right": "#FF7F00"}
        ).scale(0.8).move_to(DOWN * 2.6)
        self.play(
            FadeOut(explanation_text_d),
            FadeIn(explanation_text_e, UP),
            matrix_group.animate.shift(RIGHT * 0.5),
            FadeOut(vector_matrix, RIGHT),
            FadeOut(object_group),
            FadeIn(new_object_group),
            Uncreate(right_to_left_arrow),
            ShowCreation(left_to_right_arrow),
        )
        self.wait(4)

        object_group = new_object_group
        explanation_text_f = Text(
            "This new method requires you to move an object from its own perspective, instead of the origin's perspective.",
            t2c={"its own perspective": "#FFFF00"}
        ).scale(0.8).move_to(DOWN * 2.6)
        self.play(
            FadeOut(explanation_text_e),
            FadeIn(explanation_text_f, UP),
        )

        # LTR: Rotate
        ltr_rotate_group = Group(
            *[Square(2 * j).set_color("#FF7F00") for j in range(4)]
        ).scale(scale, about_point=ORIGIN).shift(center)
        self.play(
            ShowCreation(ltr_rotate_group),
            run_time = 1
        )
        self.wait(0.5)

        self.play(
            Indicate(matrices[0], color="#FF7F00"),
            Rotate(
                grid_group,
                -pi / 4,
                about_point = center
            ),
            run_time = 2
        )
        self.play(
            Uncreate(ltr_rotate_group),
            run_time = 1
        )

        # LTR: Translate
        ltr_translate_group = Group(
            Arrow(stroke_width=8).put_start_and_end_on(ORIGIN, RIGHT * 2).set_color("#FF7F00"),
            Arrow(stroke_width=8).put_start_and_end_on(RIGHT * 2, RIGHT * 2 + UP).set_color("#FF7F00"),
        ).scale(scale, about_point=ORIGIN).shift(center)
        self.play(
            ShowCreation(ltr_translate_group),
            run_time = 1
        )
        self.wait(0.5)

        self.play(
            Indicate(matrices[1], color="#FF7F00"),
            grid_group.animate.shift((-2 * scale, -scale, 0)),
            ltr_translate_group.animate.shift((-2 * scale, -scale, 0)),
            run_time = 2
        )
        self.play(
            Uncreate(ltr_translate_group),
            run_time = 1
        )
        self.wait(0.5)

        # LTR: Scale
        ltr_scale_group = Group(
            *[Circle(radius=j).set_color("#FF7F00") for j in range(4)]
        ).scale(scale, about_point=ORIGIN).shift(center)
        self.play(
            ShowCreation(ltr_scale_group),
            run_time = 1
        )
        self.wait(0.5)

        self.play(
            Indicate(matrices[2], color="#FF7F00"),
            grid_group.animate.scale(
                2,
                about_point = center
            ),
            run_time = 2
        )
        self.play(
            Uncreate(ltr_scale_group),
            run_time = 1
        )
        self.wait(0.5)

        explanation_text_g = Text(
            "Relative to the grid, the object is in the exact same spot as before. Rewind the video to check it out."
        ).scale(0.8).move_to(DOWN * 2.6)
        self.play(
            FadeOut(explanation_text_f),
            FadeIn(explanation_text_g, UP),
        )
        self.wait(4)

        explanation_text_h = Text(
            "With this kind of movement, every move is relative to\nthe object being transformed.\nDirections depend on its current angle and size, and the center of rotation/scaling is the object itself.",
            t2c={"relative to\nthe object": "#FFFF00"}
        ).scale(0.8).move_to(DOWN * 2.6)
        self.play(
            FadeOut(explanation_text_g),
            FadeIn(explanation_text_h, UP),
        )
        self.wait(6)

        old_objects = self.all_objects()
        right_to_left_arrow = Arrow().put_start_and_end_on(np.array([5, 2, 0]), np.array([-5, 2, 0])).set_color("#00BFFF")
        right_to_left_text = Text("From perspective of origin", color="#00BFFF").scale(0.75).move_to((0, 2.4, 0))
        left_to_right_arrow = Arrow().put_start_and_end_on(np.array([-5, 0.8, 0]), np.array([5, 0.8, 0])).set_color("#FF7F00")
        left_to_right_text = Text("From perspective of object", color="#FF7F00").scale(0.75).move_to((0, 1.2, 0))
        explanation_text_i = Text(
            "Depending on the situation, either of these reading orders might feel more intuitive to you. You can always use either interpretation.",
        ).scale(0.8).move_to(DOWN * 1.5)
        self.play(
            FadeOut(old_objects),
            ShowCreation(right_to_left_arrow),
            ShowCreation(left_to_right_arrow),
            FadeIn(right_to_left_text),
            FadeIn(left_to_right_text),
            FadeIn(explanation_text_i, UP),
        )
        self.wait(6)

        explanation_text_j = Text(
            "It is just important to know the difference between the two, to avoid making mistakes or brute-forcing your transformations.",
            t2c={"know the difference": "#FFFF00"}
        ).scale(0.8).move_to(DOWN * 1.5)
        self.play(
            FadeOut(explanation_text_i),
            FadeIn(explanation_text_j, UP),
        )
        self.wait(2)

class AlphaBlendScene(CGScene):
    def get_title(self):
        return "Alpha Blending"
    
    def animate(self):
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
            *self.swap_caption("Transparency of colors is handled by assigning an \"alpha\" value to it, which indicates the opacity of the color.")
        )
        self.wait(3.5)

        self.play(
            *self.swap_caption("When multiple objects overlap in front of the camera, their alpha values are used to determine the resulting color.")
        )

        def set_alpha(alpha):
            return [
                self.alpha_slider_triangle.animate.move_to(RIGHT * (8 * alpha - 4) + DOWN * 1.6),
                self.blue_square.animate.set_fill(opacity=alpha)
            ]
        
        self.wait(1)
        self.play(
            *set_alpha(0.2),
            run_time = 1.5
        )
        self.wait(0.5)
        self.play(
            *set_alpha(0.7),
            run_time = 1.5
        )
        self.wait(1.5)

        self.play(
            *set_alpha(0.0),
            *self.swap_caption("An alpha of 0.0 means the color is completely invisible."),
            run_time = 1.5
        )
        self.wait(3)
        
        self.play(
            *set_alpha(1.0),
            *self.swap_caption("An alpha of 1.0 means the color is opaque and not transparent at all."),
            run_time = 1.5
        )
        self.wait(3)

        self.bar_parts_rectangle = Rectangle(1, 4, color="#BFBFBF", fill_opacity=1).set_fill("#000000").shift(RIGHT * 2 + 0.5 * UP)
        self.bar_blend_rectangle = Rectangle(1, 4, color="#BFBFBF", fill_opacity=1).set_fill("#000000").shift(RIGHT * 0.5 + 0.5 * UP)
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

        self.red = self.green = self.blue = 0.0
        self.rectangle_group = Group(
            Rectangle(1, 4, color="#BFBFBF", fill_opacity=1).set_fill("#000000").move_to(self.bar_parts_rectangle)
        )

        self.green_contributes_group = Group()
        def add_alpha(alpha, color, circle_pos, iteration):
            # Create rectangle and circle
            rectangle = Rectangle(1, 4 * alpha, color="#BFBFBF", fill_opacity=1).set_fill(color).move_to(self.bar_parts_rectangle).shift(2.5 * RIGHT + 2 * (1.0 - alpha) * DOWN)
            circle = Circle(radius=1.2, color=color, stroke_opacity=alpha, fill_opacity=0).move_to(self.black_background.get_center() + circle_pos).set_fill(color)
            color_text = Text(f"alpha = {alpha}").scale(0.6).next_to(rectangle, UP)
            self.play(
                ShowCreation(circle),
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

            # Move other rectangles
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
                parenthesis_left = Tex("(").scale(0.6 + iteration * 0.15).next_to(self.formula_group, LEFT, buff=0.1)
                parenthesis_right = Tex(")").scale(0.6 + iteration * 0.15).next_to(self.formula_group, RIGHT, buff=0.1)
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
            formula_text_a = Tex(f"\cdot \, {1.0 - alpha:.1}").scale(0.6).next_to(self.formula_group, RIGHT, buff=0.1)
            self.formula_group.add(formula_text_a)
            if iteration > 1:
                self.green_contributes_group.add(formula_text_a)
            self.play(
                self.bar_blend_rectangle.animate.set_fill(rgb_to_color((self.red, self.green, self.blue)), opacity=1),
                MoveToTarget(self.rectangle_group),
                FadeIn(formula_text_a, LEFT),
                run_time = 0.8
            )
            
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
            formula_text_b = Tex("+").scale(0.6).next_to(self.formula_group, RIGHT, buff=0.1)
            formula_square = Square(side_length=0.32, color="#BFBFBF", fill_opacity=1).set_fill(color).next_to(formula_text_b, RIGHT, buff=0.1)
            formula_text_c = Tex(f"\cdot \, {alpha:.2}").scale(0.6).next_to(formula_square, RIGHT, buff=0.1)
            if iteration == 1:
                self.green_contributes_group.add(formula_text_c)
            self.formula_group.add(formula_text_b, formula_square, formula_text_c)
            self.play(
                FadeOut(brace),
                self.bar_blend_rectangle.animate.set_fill(rgb_to_color((self.red, self.green, self.blue)), opacity=1),
                rectangle.animate.shift(2.5 * LEFT),
                FadeOut(color_text),
                MoveToTarget(circle),
                FadeIn(formula_text_b, LEFT),
                FadeIn(formula_square, LEFT),
                FadeIn(formula_text_c, LEFT),
                run_time = 0.8
            )
            self.wait(1.5)

            if iteration == 0:
                self.play(
                    *self.swap_caption("With an alpha of 0.8, the resulting color is 80% the new color and 20% the old color.", pos=DOWN * 3)
                )
                self.wait(4)

            self.rectangle_group.add(rectangle)

        add_alpha(0.8, "#FF0000", LEFT * 0.5, 0)
        self.play(
            *self.swap_caption("This process is repeated when other colors overlap as well.", pos=DOWN * 3)
        )
        self.wait(0.5)

        add_alpha(0.4, "#00FF00", RIGHT * 0.5, 1)
        add_alpha(0.5, "#007FFF", UP * 0.5, 2)
        add_alpha(0.3, "#FF7F00", DOWN * 0.5, 3)

        left_center = self.black_background.get_center()
        right_center = self.bar_blend_rectangle.get_center()
        center_center = (left_center + right_center) / 2
        final_color = rgb_to_color((self.red, self.green, self.blue))

        connecting_rectangle = Rectangle(0.01, 0.4, stroke_opacity=0, fill_opacity=1).move_to(center_center).set_fill(final_color)
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
        self.wait(2)

RENDER = True
ANIMATION = "AlphaBlendScene"
SKIP_TO = 0

if __name__ == "__main__":
    if RENDER:
        os.system(f"manim-render {DIRECTORY}/main.py {ANIMATION} -w --hd --frame_rate 60")
    else:
        os.system(f"manimgl {DIRECTORY}/main.py {ANIMATION} -l -n {SKIP_TO}")