from imports import *
from manim import *
from math import pi

BLUE = "#00BFFF"
ORANGE = "#FF7F00"
YELLOW = "#FFFF00"
LIGHT_YELLOW = "#FFFF3F"

class MainScene(CGScene):
    def get_title(self):
        return "Right-To-Left or Left-To-Right?"

    def generate_object(self):
        points = [
            (8, 12),
            (9, 12),
            (9, 14),
            (10, 14),
            (10, 15),
            (12, 15),
            (12, 16),
            (14, 16),
            (14, 15),
            (15, 15),
            (15, 14),
            (16, 14),
            (16, 6),
            (14, 6),
            (14, 4),
            (12, 4),
            (12, 2),
            (10, 2),
            (10, 0),
            (6, 0),
            (6, 2),
            (4, 2),
            (4, 4),
            (2, 4),
            (2, 6),
            (0, 6),
            (0, 14),
            (1, 14),
            (1, 15),
            (2, 15),
            (2, 16),
            (4, 16),
            (4, 15),
            (6, 15),
            (6, 14),
            (7, 14),
            (7, 12),
        ]

        edges = Group()
        for i in range(len(points)):
            a = np.array([*points[i], 0])
            b = np.array([*points[(i + 1) % len(points)], 0])

            edge = Line(a, b).set_color(LIGHT_YELLOW)
            edges.add(edge)

        edges.shift((-8, -8, 0)).scale(0.2)
        return edges

    def animate(self):
        # Show matrix list
        matrices = [
            Matrix(
                [["\cos(\pi / 4)", "-\sin(\pi / 4)", "0"], ["\sin(\pi / 4)", "\cos(\pi / 4)", "0"], ["0", "0", "1"]],
                element_alignment_corner=ORIGIN,
                h_buff=2.2
            ),
            Matrix(
                [["1", "0", "2"], ["0", "1", "1"], ["0", "0", "1"]],
                element_alignment_corner=ORIGIN,
                h_buff=0.8
            ),
            Matrix(
                [["1/2", "0", "0"], ["0", "1/2", "0"], ["0", "0", "1"]],
                element_alignment_corner=ORIGIN,
                h_buff=0.8
            ),
        ]
        matrix_descriptions_texts = [
            Text("Rotate by π/4"),
            Text("Translate by (2, 1)"),
            Text("Scale by 1/2"),
        ]
        matrix_group = Group(*matrices)
        matrix_group.arrange(RIGHT)
        for i in range(len(matrix_descriptions_texts)):
            matrix_descriptions_texts[i].scale(0.6).next_to(matrices[i], UP).set_color("#BFBFBF")
        matrix_group.add(*matrix_descriptions_texts)
        matrix_group.scale(0.9).move_to(UP * 0.5)
        self.play(
            FadeIn(matrix_group)
        )
        self.play(
            *self.swap_caption(
                "Suppose we have a few operations, each with their own transformation matrix."
            )
        )
        self.wait(4)

        # Show grid
        scale = 0.7
        center = np.array([3.2, -1, 0])
        grid_group = self.generate_grid(((-1, 5), (-1, 5)))
        grid_group.scale(scale, about_point=ORIGIN).shift(center)
        object_group = self.generate_object()
        object_group.scale(scale, about_point=ORIGIN).shift(center)

        matrix_group.generate_target()
        matrix_group.target.scale(0.75)
        matrix_group.target.shift(UP * 1)

        result_matrix = Matrix(
            [["\\frac{1}{2}\cos(\\frac{\pi}{4})", "-\\frac{1}{2}\sin(\\frac{\pi}{4})", "2\cos(\\frac{\pi}{4}) - \sin(\\frac{\pi}{4})"], ["\\frac{1}{2}\sin(\\frac{\pi}{4})", "\\frac{1}{2}\cos(\\frac{\pi}{4})", "2\sin(\\frac{\pi}{4}) + \cos(\\frac{\pi}{4})"], ["0", "0", "1"]],
            element_alignment_corner=ORIGIN,
            h_buff=3.6,
            v_buff=1.4
        )
        result_matrix.scale(0.5).next_to(matrix_group.target, DOWN).shift(0.1 * RIGHT)
        equals_text = Tex("$=$")
        equals_text.next_to(result_matrix, LEFT)
        result_group = Group(result_matrix, equals_text)

        self.play(
            *self.swap_caption(
                "When multiplying these matrices, we'll get one huge matrix that does all of these operations in one go."
            ),
            MoveToTarget(matrix_group)
        )
        self.wait(0.5)
        self.play(
            FadeIn(result_group, shift=UP * 0.5),
        )
        self.wait(2.5)

        self.play(
            *self.swap_caption(
                "The huge matrix in this scenario performs the following transformation."
            ),
            matrix_group.animate.shift(LEFT * 2.5),
            result_group.animate.shift(LEFT * 2.5),
            FadeIn(grid_group, shift=LEFT),
            FadeIn(object_group, shift=LEFT),
        )
        self.wait(1.5)

        backup_object_group = Group(*[obj.copy() for obj in object_group])

        goal_object_group = Group(*[obj.copy() for obj in object_group])
        goal_object_group.generate_target()
        goal_object_group.target.scale(0.5, about_point=center).shift(np.array([2, 1, 0]) * scale).rotate(pi / 4, about_point=center)
        for obj in object_group:
            obj.set_stroke("#7F7F7F")

        self.play(
            MoveToTarget(goal_object_group),
            Indicate(result_matrix, 1.15, LIGHT_YELLOW),
            run_time=2
        )
        self.wait(2)

        self.play(
            *self.swap_caption(
                "But in what order has the huge matrix then performed the three operations? Right-to-left or left-to-right?",
                t2c={"what": YELLOW, "order": YELLOW, "Right-to-left": BLUE, "left-to-right": ORANGE}
            ),
            result_group.animate.set_color("#7F7F7F").shift(DOWN * 1)
        )

        y = matrices[0].get_bottom()[1]
        x1 = matrices[0].get_left()[0]
        x2 = matrices[2].get_right()[0]
        right_to_left_arrow = Arrow(stroke_width=6, max_stroke_width_to_length_ratio=1e9).set_color(BLUE).put_start_and_end_on((x2, y - 0.25, 0), (x1, y - 0.25, 0))
        left_to_right_arrow = Arrow(stroke_width=6, max_stroke_width_to_length_ratio=1e9).set_color(ORANGE).put_start_and_end_on((x1, y - 0.5, 0), (x2, y - 0.5, 0))
        self.play(
            self.appear(right_to_left_arrow),
            self.appear(left_to_right_arrow),
        )
        self.wait(4)

        def scale_object(object_group, color, matrix, factor, animation_time):
            help_lines = Group(
                *[Square(2 * j).set_color(color) for j in range(4)]
            )
            help_lines.scale(scale, about_point=ORIGIN).shift(center)
            self.play(
                *[self.appear(j) for j in help_lines],
                matrix.animate.set_color(color).scale(1.15),
                run_time=0.5
            )
            self.wait(0.5)

            self.play(
                object_group.animate.scale(
                    factor,
                    about_point=center
                ),
                help_lines.animate.scale(
                    factor,
                    about_point=center
                ),
                run_time=animation_time
            )
            self.play(
                *[self.disappear(j) for j in help_lines],
                matrix.animate.set_color("#FFFFFF").scale(1 / 1.15),
                run_time=0.5
            )

        def translate_object(object_group, color, matrix, shift, animation_time):
            help_dot = Circle(0.1).set_stroke(opacity=0).set_fill(color, opacity=1)
            help_lines = Group(
                help_dot,
                Arrow(stroke_width=4, max_stroke_width_to_length_ratio=1e9, max_tip_length_to_length_ratio=0.25).set_color(color).put_start_and_end_on(ORIGIN, RIGHT * shift[0]),
                Arrow(stroke_width=4, max_stroke_width_to_length_ratio=1e9, max_tip_length_to_length_ratio=0.25).set_color(color).put_start_and_end_on(RIGHT * shift[0], shift),
            )
            help_lines.scale(scale, about_point=ORIGIN).shift(center)
            self.play(
                *[self.appear(j) for j in help_lines],
                matrix.animate.set_color(color).scale(1.15),
                run_time=0.5
            )
            self.wait(0.5)

            self.play(
                object_group.animate.shift(
                    shift * scale
                ),
                help_dot.animate.shift(
                    shift * scale
                ),
                run_time=animation_time
            )
            self.play(
                *[self.disappear(j) for j in help_lines],
                matrix.animate.set_color("#FFFFFF").scale(1 / 1.15),
                run_time=0.5
            )

        def rotate_object(object_group, color, matrix, angle, animation_time):
            help_lines = Group(
                *[Circle(j).set_color(color) for j in range(4)],
                Line(LEFT * 3, RIGHT * 3).set_color(color),
                Line(DOWN * 3, UP * 3).set_color(color),
            )
            help_lines.scale(scale, about_point=ORIGIN).shift(center)
            self.play(
                *[self.appear(j) for j in help_lines],
                matrix.animate.set_color(color).scale(1.15),
                run_time=0.5
            )
            self.wait(0.5)

            self.play(
                Rotate(
                    object_group,
                    angle,
                    about_point=center
                ),
                Rotate(
                    help_lines,
                    angle,
                    about_point=center
                ),
                run_time=animation_time
            )
            self.play(
                *[self.disappear(j) for j in help_lines],
                matrix.animate.set_color("#FFFFFF").scale(1 / 1.15),
                run_time=0.5
            )

        # RTL
        self.bring_to_front(object_group)
        arrow_to_disappear, left_to_right_arrow = left_to_right_arrow, left_to_right_arrow.copy()
        self.play(
            *self.swap_caption(
                "The general answer is right-to-left; if we apply the transformation in that order, the following happens.",
                t2c={"right-to-left": BLUE}
            ),
            goal_object_group.animate.set_color("#7F7F7F"),
            object_group.animate.set_color(LIGHT_YELLOW),
            self.disappear(arrow_to_disappear),
        )
        self.wait(1)

        # RTL: Scale
        scale_object(object_group, BLUE, matrices[2], 0.5, 1.6)

        # RTL: Translate
        translate_object(object_group, BLUE, matrices[1], np.array([2, 1, 0]), 1.6)

        # RTL: Rotate
        rotate_object(object_group, BLUE, matrices[0], pi / 4, 1.6)

        self.wait(0.5)

        self.play(
            *self.swap_caption(
                "Having applied each operation individually, we get the same result as with the huge matrix from before.",
                t2c={"same": YELLOW, "result": YELLOW}
            ),
        )
        self.wait(4)

        # RTL
        old_object_group = object_group
        wrong_object_group = Group(*[obj.copy() for obj in backup_object_group])
        self.play(
            *self.swap_caption(
                "Reading left-to-right does not get us the same result.",
                t2c={"left-to-right": ORANGE},
                t2s={"not": ITALIC}
            ),
            FadeOut(old_object_group),
            FadeIn(wrong_object_group),
            self.appear(left_to_right_arrow),
            self.disappear(right_to_left_arrow),
        )
        self.wait(0.5)

        # LTR (wrong): Rotate
        rotate_object(wrong_object_group, ORANGE, matrices[0], pi / 4, 0.8)

        # LTR (wrong): Translate
        translate_object(wrong_object_group, ORANGE, matrices[1], np.array([2, 1, 0]), 0.8)

        # LTR (wrong): Scale
        scale_object(wrong_object_group, ORANGE, matrices[2], 0.5, 0.8)

        self.wait(1)

        self.play(
            *self.swap_caption(
                "Thinking that matrices are read left-to-right generally leads to mistakes, so be careful of this.",
                t2c={"left-to-right": ORANGE, "mistakes": "#FF3F3F"}
            ),
            wrong_object_group.animate.set_color("#FF3F3F"),
        )
        self.wait(4)

        self.play(
            *self.swap_caption(
                "However, there is a different way of imagining movement for which left-to-right reading does work.",
                t2c={"different": YELLOW, "imagining": YELLOW, "movement": YELLOW, "left-to-right": ORANGE},
                t2s={"does": ITALIC}
            ),
        )
        self.wait(1)

        object_group = Group(*[obj.copy() for obj in backup_object_group])
        self.bring_to_front(object_group)
        self.play(
            FadeOut(wrong_object_group),
            FadeIn(object_group)
        )
        self.wait(2.5)

        self.play(
            *self.swap_caption(
                "To start off, we will draw two unit vectors, which are located at the origin.",
                t2c={"unit": YELLOW, "vectors": YELLOW, "origin": YELLOW}
            ),
        )
        self.wait(1)

        x_arrow = Arrow(stroke_width=4, max_stroke_width_to_length_ratio=1e9, max_tip_length_to_length_ratio=0.15).set_color("#FF0000")
        x_arrow.put_start_and_end_on(center, center + RIGHT).scale(scale, about_point=center)
        x_ghost_arrow = x_arrow.copy().set_fill(opacity=0.5).set_stroke(opacity=0.5)
        y_arrow = Arrow(stroke_width=4, max_stroke_width_to_length_ratio=1e9, max_tip_length_to_length_ratio=0.15).set_color("#00FF00")
        y_arrow.put_start_and_end_on(center, center + UP).scale(scale, about_point=center)
        y_ghost_arrow = y_arrow.copy().set_fill(opacity=0.5).set_stroke(opacity=0.5)
        object_group.add(x_arrow, y_arrow)
        self.play(
            self.appear(x_arrow),
            self.appear(y_arrow),
            run_time=0.6
        )
        self.wait(2)

        self.add(x_ghost_arrow)
        self.add(y_ghost_arrow)
        self.bring_to_front(x_arrow)
        self.bring_to_front(y_arrow)
        to_move_group = Group(
            grid_group,
            goal_object_group,
            object_group
        )

        self.play(
            *self.swap_caption(
                "After each operation, we shift our perspective such that the two vectors are back where they were before.",
                t2c={"shift": YELLOW, "our": YELLOW, "perspective": YELLOW}
            ),
        )
        self.wait(0.5)

        # LTR: Rotate
        rotate_object(object_group, ORANGE, matrices[0], pi / 4, 1.2)
        self.wait(0.5)
        self.play(
            Rotate(
                to_move_group,
                -pi / 4,
                about_point=center
            ),
            run_time=1
        )
        self.wait(2)

        self.play(
            *self.swap_caption(
                "Then, we'll continue to the next operation, pretending the two vectors are still the unit vectors.",
                t2s={"still": ITALIC}
            ),
        )
        self.wait(1)

        # LTR: Translate
        translate_object(object_group, ORANGE, matrices[1], np.array([2, 1, 0]), 2)
        self.wait(1)

        self.play(
            *self.swap_caption(
                "Note how the translation we just made doesn't align with the grid, but does align with the vectors.",
                t2s={"does": ITALIC, "n't": ITALIC}
            ),
        )
        self.wait(4)

        self.play(
            *self.swap_caption(
                "After applying more operations and shifting our perspective, we end up with the correct result.",
                t2c={"still": YELLOW, "unit": YELLOW, "vectors": YELLOW}
            ),
            to_move_group.animate.shift(np.array([2, 1, 0]) * -scale),
            run_time=1
        )

        self.wait(1)

        # LTR: Scale
        scale_object(object_group, ORANGE, matrices[2], 0.5, 1.2)
        self.wait(0.5)
        self.play(
            to_move_group.animate.scale(2, about_point=center),
            run_time=1
        )
        self.remove(goal_object_group)
        self.remove(x_ghost_arrow)
        self.remove(y_ghost_arrow)
        self.wait(3)

        to_move_back_group = Group(
            grid_group,
            object_group,
        )
        to_move_back_group.generate_target()
        to_move_back_group.target.scale(0.5, about_point=center)
        to_move_back_group.target.shift(np.array([2, 1, 0]) * scale)
        to_move_back_group.target.rotate(pi / 4, about_point=center)
        self.play(
            *self.swap_caption(
                "If we constantly realign ourselves with the object we're transforming, reading left-to-right is the way to go.",
                t2c={"left-to-right": ORANGE}
            ),
            MoveToTarget(to_move_back_group),
            run_time=1
        )
        self.wait(4)

        to_fade_out_group = Group(
            grid_group,
            object_group,
            result_group,
            left_to_right_arrow
        )
        self.play(
            *self.swap_caption(
                "To summarize: when staying aligned with the grid, you read matrix chains by applying them right-to-left.",
                t2c={"right-to-left": BLUE, "grid": YELLOW}
            ),
            FadeOut(to_fade_out_group),
            matrix_group.animate.scale(1.2).move_to(UP * 0.5)
        )
        self.wait(0.5)
        
        y1 = matrix_descriptions_texts[0].get_top()[1]
        y2 = matrices[0].get_bottom()[1]
        x1 = matrices[0].get_left()[0]
        x2 = matrices[2].get_right()[0]
        right_to_left_arrow = Arrow(stroke_width=6, max_stroke_width_to_length_ratio=1e9).set_color(BLUE).put_start_and_end_on((x2, y1 + 0.3, 0), (x1, y1 + 0.3, 0))
        left_to_right_arrow = Arrow(stroke_width=6, max_stroke_width_to_length_ratio=1e9).set_color(ORANGE).put_start_and_end_on((x1, y2 - 0.3, 0), (x2, y2 - 0.3, 0))
        right_to_left_text = Text("Aligned with grid", color=BLUE).scale(0.7).next_to(right_to_left_arrow, UP)
        left_to_right_text = Text("Aligned with object", color=ORANGE).scale(0.7).next_to(left_to_right_arrow, DOWN)

        self.play(
            self.appear(right_to_left_arrow),
            Write(right_to_left_text)
        )
        self.wait(3.5)

        self.play(
            *self.swap_caption(
                "However, if you keep yourself aligned with the object, you should read operations in a matrix chain left-to-right.",
                t2c={"left-to-right": ORANGE, "object": YELLOW}
            ),
            self.appear(left_to_right_arrow),
            Write(left_to_right_text)
        )
        self.wait(3)

HIGH_QUALITY = True
START_AT = 0
END_AT = 1000

if __name__ == "__main__":
    render_video(os.path.realpath(__file__), HIGH_QUALITY, START_AT, END_AT)