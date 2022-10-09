from imports import *
from manim import *
from math import pi

class MainScene(CGScene):
    def get_title(self):
        return "Right-To-Left or Left-To-Right?"

    def animate(self):
        # Show matrix list
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
        self.play(
            *self.swap_caption(
                "Suppose we have a few operations strung together by multiplying their matrices."
            )
        )
        self.wait(4)

        # Show grid
        scale = 0.7
        center = np.array([-6, -1, 0])
        grid_group = self.generate_grid(((-1, 5), (-1, 5))).scale(scale, about_point=ORIGIN).shift(center)
        object_group = self.generate_crosshairs().scale(scale, about_point=ORIGIN).shift(center)
        right_to_left_arrow = Arrow((6.7, 0.3, 0), (-1.7, 0.3, 0)).set_color("#00BFFF")
        left_to_right_arrow = Arrow((-1.7, 0, 0), (6.7, 0, 0)).set_color("#FF7F00")
        matrix_group.generate_target()
        matrix_group.target.scale(0.75)
        matrix_group.target.shift(RIGHT * 2.5 + UP * 0.5)
        self.play(
            *self.swap_caption(
                "When applying these operations one at a time, should we read them right-to-left or left-to-right?",
                t2c={"right-to-left": "#00BFFF", "left-to-right": "#FF7F00"}
            ),
            Create(right_to_left_arrow),
            Create(left_to_right_arrow),
            FadeIn(grid_group),
            FadeIn(object_group),
            MoveToTarget(matrix_group)
        )
        self.wait(4)

        # RTL
        self.play(
            *self.swap_caption(
                "The usual way is right-to-left, as long as each operation is done from the perspective of the origin.",
                t2c={"right-to-left": "#00BFFF", "perspective of the origin": "#FFFF00"}
            ),
            FadeOut(left_to_right_arrow),
        )

        # RTL: Scale
        rtl_scale_group = Group(
            *[Square(2 * j).set_color("#00BFFF") for j in range(4)]
        ).scale(scale, about_point=ORIGIN).shift(center)
        self.play(
            *[Create(j) for j in rtl_scale_group],
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
            *[Uncreate(j) for j in rtl_scale_group],
            run_time = 1
        )

        # RTL: Translate
        rtl_translate_group = Group(
            Arrow(stroke_width=8).put_start_and_end_on(ORIGIN, RIGHT * 2).set_color("#00BFFF"),
            Arrow(stroke_width=8).put_start_and_end_on(RIGHT * 2, RIGHT * 2 + UP).set_color("#00BFFF"),
        ).scale(scale, about_point=ORIGIN).shift(center)
        self.play(
            *[Create(j) for j in rtl_translate_group],
            run_time = 1
        )
        self.wait(0.5)

        self.play(
            Indicate(matrices[1], color="#00BFFF"),
            object_group.animate.shift((2 * scale, scale, 0)),
            run_time = 2
        )
        self.play(
            *[Uncreate(j) for j in rtl_translate_group],
            run_time = 1
        )

        # RTL: Rotate
        rtl_rotate_group = Group(
            *[Circle(radius=j).set_color("#00BFFF") for j in range(4)]
        ).scale(scale, about_point=ORIGIN).shift(center)
        self.play(
            *[Create(j) for j in rtl_rotate_group],
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
            *[Uncreate(j) for j in rtl_rotate_group],
            run_time = 1
        )
        self.wait(0.5)

        # Show vector
        vector_matrix = Matrix([["x"], ["y"], ["1"]]).scale(0.75).next_to(matrices[2], RIGHT).shift(LEFT * 1.1).set_color("#FF00FF")
        self.play(
            *self.swap_caption(
                "Right-to-left also makes sense in the math, since the matrix that is closest to the vector (on the right) is multiplied first.",
                t2c={"Right-to-left": "#00BFFF", "vector": "#FF00FF"}
            ),
            matrix_group.animate.shift(LEFT),
            FadeIn(vector_matrix, shift=LEFT),
            run_time = 1
        )
        self.wait(4)

        # Introduce LTR
        new_object_group = self.generate_crosshairs().scale(scale, about_point=ORIGIN).shift(center)
        self.play(
            *self.swap_caption(
                "However, there is also a different method of applying operations, for which left-to-right reading can be used.",
                t2c={"left-to-right": "#FF7F00"}
            ),
            matrix_group.animate.shift(RIGHT),
            FadeOut(vector_matrix, shift=RIGHT),
            FadeOut(object_group),
            FadeIn(new_object_group),
            Uncreate(right_to_left_arrow),
            Create(left_to_right_arrow),
        )
        self.wait(4)

        # LTR
        object_group = new_object_group
        self.play(
            *self.swap_caption(
                "This new method requires us to move an object from its own perspective, instead of the origin's perspective.",
                t2c={"its own perspective": "#FFFF00"}
            ),
        )

        # LTR: Rotate
        ltr_rotate_group = Group(
            *[Circle(radius=j).set_color("#FF7F00") for j in range(4)]
        ).scale(scale, about_point=ORIGIN).shift(center)
        self.play(
            *[Create(j) for j in ltr_rotate_group],
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
            *[Uncreate(j) for j in ltr_rotate_group],
            run_time = 1
        )

        # LTR: Translate
        ltr_translate_group = Group(
            Arrow(stroke_width=8).put_start_and_end_on(ORIGIN, RIGHT * 2).set_color("#FF7F00"),
            Arrow(stroke_width=8).put_start_and_end_on(RIGHT * 2, RIGHT * 2 + UP).set_color("#FF7F00"),
        ).scale(scale, about_point=ORIGIN).shift(center)
        self.play(
            *[Create(j) for j in ltr_translate_group],
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
            *[Uncreate(j) for j in ltr_translate_group],
            run_time = 1
        )
        self.wait(0.5)

        # LTR: Scale
        ltr_scale_group = Group(
            *[Square(2 * j).set_color("#FF7F00") for j in range(4)]
        ).scale(scale, about_point=ORIGIN).shift(center)
        self.play(
            *[Create(j) for j in ltr_scale_group],
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
            *[Uncreate(j) for j in ltr_scale_group],
            run_time = 1
        )
        self.wait(0.5)

        self.play(
            *self.swap_caption(
                "Relative to the grid, the object is in the exact same spot as before. Rewind the video to check it out."
            ),
        )
        self.wait(4)

        self.play(
            *self.swap_caption(
                "With this kind of movement, every move is relative to the object being transformed. Directions depend on its current angle and size, and the center of rotation/scaling is the object itself.",
                t2c={"relative to\nthe object": "#FFFF00"}
            ),
        )
        self.wait(6)

        # Show summary
        old_objects = self.all_objects()
        right_to_left_arrow = Arrow().put_start_and_end_on(np.array([5, 1.4, 0]), np.array([-5, 1.4, 0])).set_color("#00BFFF")
        right_to_left_text = Text("From perspective of origin", color="#00BFFF").scale(0.75).move_to((0, 1.8, 0))
        left_to_right_arrow = Arrow().put_start_and_end_on(np.array([-5, 0.2, 0]), np.array([5, 0.2, 0])).set_color("#FF7F00")
        left_to_right_text = Text("From perspective of object", color="#FF7F00").scale(0.75).move_to((0, 0.6, 0))
        self.play(
            FadeOut(old_objects),
            Create(right_to_left_arrow),
            Create(left_to_right_arrow),
            FadeIn(right_to_left_text),
            FadeIn(left_to_right_text),
            *self.swap_caption(
                "Depending on the situation, either of these reading orders might feel more intuitive to you. You can always use either interpretation.",
            )
        )
        self.wait(6)

        # Show motivation
        self.play(
            *self.swap_caption(
                "It is just important to know the difference between the two, to avoid making mistakes or brute-forcing your transformations.",
                t2c={"know the difference": "#FFFF00"}
            ),
        )
        self.wait(2)

HIGH_QUALITY = False
START_AT = 0
END_AT = 1000

if __name__ == "__main__":
    render_video(os.path.realpath(__file__), HIGH_QUALITY, START_AT, END_AT)