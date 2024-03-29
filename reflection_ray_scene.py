from imports import *
from manim import *
from math import pi, sqrt

class MainScene(CGScene):
    def get_title(self):
        return "Reflection Ray Formula"

    def animate(self):
        # Show mirror, N and L
        mirror_group = Group()
        mirror_line = Line(LEFT * 5, RIGHT * 5, color="#FFFFFF")
        mirror_text = Text("Mirror", color="#FFFFFF").move_to(0.3 * UP + 4 * LEFT).scale(0.65)
        mirror_group.add(mirror_line, mirror_text)
        iterations = 15
        for i in range(iterations):
            x = (i - iterations // 2) * 0.65
            diagonal_line = Line(RIGHT * x + LEFT * 0.1 + DOWN * 0.2, RIGHT * x + RIGHT * 0.1)
            mirror_group.add(diagonal_line)

        normal_group = Group()
        normal_arrow = Arrow().put_start_and_end_on((0, 0, 0), UP * 4)
        normal_arrow.set_color("#FF7F00")
        normal_text = Tex("$\hat{N}$", color="#FF7F00").move_to(LEFT * 0.3 + UP * 3.5)
        normal_group.add(normal_arrow, normal_text)

        light_group = Group()
        light_arrow = Arrow().put_start_and_end_on((0, 0, 0), LEFT * sqrt(12) + UP * 2).set_color("#FFFF00")
        light_text = Tex("$\hat{L}$", color="#FFFF00").move_to(LEFT * sqrt(12) + UP * 1.6)
        light_group.add(light_arrow, light_text)
        light_group.shift((-sqrt(3) * 5, 5, 0))
        sun_image = ImageMobject(self.get_asset("sun.png")).scale(0.2).move_to(LEFT * sqrt(12) * 1.25 + UP * 2.5)
        self.play(
            FadeIn(mirror_group),
            FadeIn(normal_group),
            FadeIn(sun_image),
            run_time=1
        )
        self.play(
            light_group.animate.shift((sqrt(3) * 5, -5, 0)),
            run_time=1
        )

        # Show R
        reflection_group = Group()
        reflection_arrow = Arrow().put_start_and_end_on((0, 0, 0), RIGHT * sqrt(12) + UP * 2).set_color("#FF007F")
        reflection_text = Tex("$R$", color="#FF007F").move_to(RIGHT * (sqrt(12) - 0.5) + UP * 2.1)
        reflection_group.add(reflection_arrow, reflection_text)
        self.play(
            Create(reflection_arrow),
            FadeIn(reflection_text),
            run_time=1
        )
        self.wait(1)

        # Show R = ?
        formula_texts = [
            Tex("$R$", color="#FF007F"),
            Tex("$=$"),
            Tex("$-\hat{L}$", color="#FFFF00"),
            Tex("$+$"),
            Tex("$2 \cdot \cos(\\angle(\hat{L}, \hat{N})) \cdot \hat{N}$", color="#FF3F00"),
        ]
        formula_group = Group(*formula_texts)
        new_formula_text = Tex("$2 \cdot \mathrm{dot}(\hat{L}, \hat{N}) \cdot \hat{N}$", color="#FF3F00")
        question_mark_text = Tex("$?$", color="#7F7F7F")
        formula_texts[0].move_to(LEFT * 5.5 + DOWN * 2)
        for i in range(1, len(formula_texts)):
            formula_texts[i].next_to(formula_texts[i - 1], RIGHT)
        new_formula_text.next_to(formula_texts[-2], RIGHT).shift((0, 0.5, 0))
        question_mark_text.next_to(formula_texts[1], RIGHT)
        self.play(
            ReplacementTransform(reflection_text.copy(), formula_texts[0]),
            FadeIn(formula_texts[1]),
            FadeIn(question_mark_text),
        )
        self.wait(1)

        # Show -L
        negative_light_arrow = light_arrow.copy().set_color("#FFFF00")
        negative_light_text = Tex("$-\hat{L}$", color="#FFFF00").move_to(RIGHT * 3.5 + DOWN * 2.2)
        negative_light_text
        self.play(
            negative_light_arrow.animate.put_start_and_end_on((0, 0, 0), RIGHT * sqrt(12) + DOWN * 2),
            ReplacementTransform(light_text.copy(), negative_light_text),
        )
        self.wait(1)

        # Show dotted line and arc
        dotted_line = DashedLine(light_arrow.get_end(), (0, *light_arrow.get_end()[1:]), dash_length=0.2)
        angle = 5 * pi / 6
        angle_arc = Arc(radius=0.5, start_angle=angle, angle=0.5 * pi - angle)
        self.play(
            Create(dotted_line),
            Create(angle_arc),
            run_time=0.6
        )
        self.wait(1)

        # Show first small normal
        small_normal_arrow_a = Arrow().put_start_and_end_on((0, 0, 0), UP * 4).set_color("#FF3F00")
        small_normal_text_a = Tex("$\cos(\\angle(\hat{L}, \hat{N})) \cdot \hat{N}$", color="#FF3F00").move_to(RIGHT * 1.3 + UP * 2).scale(0.6)
        self.play(
            small_normal_arrow_a.animate.put_start_and_end_on(LEFT - LEFT, (0, light_arrow.get_end()[1], 0)),
            ReplacementTransform(normal_text.copy(), small_normal_text_a),
        )
        self.wait(1)

        # Move small normals
        self.add(small_normal_arrow_a.copy())
        self.play(
            small_normal_arrow_a.animate.shift(negative_light_arrow.get_end()),
            small_normal_text_a.animate.shift(negative_light_arrow.get_end() + DOWN * 0.4),
            run_time=0.6
        )
        small_normal_arrow_b = small_normal_arrow_a.copy()
        small_normal_text_b = small_normal_text_a.copy()
        self.play(
            small_normal_arrow_b.animate.shift((0, -negative_light_arrow.get_end()[1], 0)),
            small_normal_text_b.animate.shift((0, -negative_light_arrow.get_end()[1], 0)),
            run_time=0.6
        )
        self.wait(1)

        # Fill in formula
        self.play(
            FadeOut(question_mark_text, shift=DOWN),
            ReplacementTransform(negative_light_text.copy(), formula_texts[2]),
            FadeIn(formula_texts[3]),
            ReplacementTransform(small_normal_text_a.copy(), formula_texts[4]),
            ReplacementTransform(small_normal_text_b.copy(), formula_texts[4]),
        )
        self.wait(2)

        # Show dot formula
        formula_group.generate_target()
        formula_group.target.scale(0.6)
        formula_group.target.shift((0, 1, 0))
        self.play(
            MoveToTarget(formula_group),
        )
        dot_formula_text = Tex("$\cos(\\angle(\hat{L}, \hat{N})) = \\frac{\mathrm{dot}(\hat{L}, \hat{N})}{|\hat{L}| \cdot |\hat{N}|} = \\frac{\mathrm{dot}(\hat{L}, \hat{N})}{1 \cdot 1} = \mathrm{dot}(\hat{L}, \hat{N})$")
        dot_formula_text.scale(0.8).shift(LEFT * 2.4 + DOWN * 2.2)
        self.play(
            Write(dot_formula_text),
            run_time=1.2
        )
        self.wait(2.5)

        # Swap cosine with dot
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
            ReplacementTransform(formula_texts[-1], new_formula_text),
        )
        self.wait(3)

        # Start explanation
        formula_group.remove(formula_texts[-1])
        formula_group.add(new_formula_text)
        formula_group.generate_target()
        formula_group.target.scale(0.8)
        formula_group.target.move_to(RIGHT + UP * 0.8)
        objects_to_delete = self.all_objects().remove(formula_group, sun_image, light_group, mirror_group)
        explanation_text_a = Text("This formula works if L is defined as pointing\nfrom surface to light source.").scale(0.7).move_to(RIGHT + UP * 1.8)
        self.play(
            *[FadeOut(j) for j in objects_to_delete],
            FadeIn(explanation_text_a),
            MoveToTarget(formula_group),
            sun_image.animate.move_to(LEFT * 5 + UP * 2),
            light_arrow.animate.put_start_and_end_on(LEFT * 5 + DOWN * 1.5, LEFT * 5 + UP * 1.5),
            light_text.animate.move_to(LEFT * 5.3),
            mirror_group.animate.move_to(LEFT * 9 + DOWN * 1.5),
            run_time=1.2
        )
        self.add(formula_group)
        self.wait(2)

        # Show alternative negative formula
        negative_formula_texts = [
            Tex("$R$", color="#FF007F"),
            Tex("$=$"),
            Tex("$\hat{L}$", color="#FFFF00"),
            Tex("$+$"),
            Tex("$-2 \cdot \mathrm{dot}(\hat{L}, \hat{N}) \cdot \hat{N}$", color="#FF3F00"),
        ]
        for i in range(1, len(negative_formula_texts)):
            negative_formula_texts[i].next_to(negative_formula_texts[i - 1], RIGHT)
        negative_formula_group = Group(*negative_formula_texts)
        negative_formula_group.scale(0.8).move_to(RIGHT + DOWN * 1.8)
        explanation_text_b = Text("If L is defined as pointing from light source\nto surface, the formula is negated:").scale(0.7).move_to(RIGHT + DOWN * 0.8)
        self.play(
            FadeIn(explanation_text_b),
            FadeIn(negative_formula_group),
            Rotate(
                light_arrow,
                pi,
                axis = np.array([0, 0, 1]),
                about_point = LEFT * 5
            ),
            run_time=1.2
        )

HIGH_QUALITY = True
START_AT = 0
END_AT = 1000

if __name__ == "__main__":
    render_video(os.path.realpath(__file__), HIGH_QUALITY, START_AT, END_AT)