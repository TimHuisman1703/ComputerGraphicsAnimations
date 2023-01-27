from imports import *
from manim import *
import random

class MainScene(CGScene):
    def get_title(self):
        return "Bilinear Interpolation"

    def animate(self):
        nearest_neighbor_texture = ImageMobject(self.get_asset("4x3_texture.png")).scale_to_fit_width(6).shift((0, 0.5, 0))
        interpolated_clamp_texture = ImageMobject(self.get_asset("4x3_texture_interpolated_clamp.png")).scale_to_fit_width(6).move_to(nearest_neighbor_texture)
        interpolated_repeat_texture = ImageMobject(self.get_asset("4x3_texture_interpolated_repeat.png")).scale_to_fit_width(6).move_to(nearest_neighbor_texture)
        interpolated_inner_texture = ImageMobject(self.get_asset("4x3_texture_interpolated_inner.png")).scale_to_fit_width(4.5).move_to(nearest_neighbor_texture)

        # Show 4x3 texture
        self.play(
            FadeIn(nearest_neighbor_texture, shift=DOWN)
        )

        self.play(
            *self.swap_caption("Textures, at their core, are a bunch of colored texels aligned in a grid."),
        )
        self.wait(3.5)

        # Draw contrast lines
        create_actions = []
        fade_out_actions = []
        for ix in range(3):
            line = Line((ix * 1.5 - 1.5, 2.75, 0), (ix * 1.5 - 1.5, -1.75, 0))
            create_actions.append(Create(line))
            fade_out_actions.append(FadeOut(line))
        for iy in range(2):
            line = Line((-3, iy * 1.5 - 0.25, 0), (3, iy * 1.5 - 0.25, 0))
            create_actions.append(Create(line))
            fade_out_actions.append(FadeOut(line))
        self.play(
            *self.swap_caption("When drawing a texture with a low resolution, the edges between these texels are very obvious."),
        )
        self.play(
            *create_actions,
            run_time=0.8
        )
        self.wait(3)

        self.play(
            *fade_out_actions,
            *self.swap_caption("Since this doesn't look as nice up close, we might want to make this color-to-color transition smoother."),
        )
        self.wait(4.5)

        self.play(
            *self.swap_caption(
                "One way to achieve this, is by applying bilinear interpolation.",
                t2c={"bilinear": "#FFFF00", "interpolation": "#FFFF00"}
            ),
        )

        # Show final version
        bilinear_interpolation_text = Tex("Interpolated").scale(0.6).set_opacity(0.5).next_to(nearest_neighbor_texture, UP)
        self.play(
            FadeIn(bilinear_interpolation_text, shift=RIGHT),
            FadeIn(interpolated_clamp_texture)
        )
        self.wait(3)

        COLORS = [
            "#EDAE49",
            "#D1495B",
            "#30638E",
            "#003D5B",
        ]
        X = 0.9
        Y = 1.2

        # Revert back to original
        self.play(
            FadeOut(bilinear_interpolation_text, shift=RIGHT),
            FadeOut(interpolated_clamp_texture),
            *self.swap_caption("How does it work? Suppose we try to sample the color from this texture at this point.")
        )

        # Place point, draw attention to it
        sample_point = Circle(radius=0.05).set_fill("#00BF00", opacity=1).set_stroke(opacity=0).move_to((-3 + 1.5 * X, 2.75 - 1.5 * Y, 0))
        sample_point.z = 10
        self.play(
            GrowFromCenter(sample_point),
            run_time=0.4
        )
        self.play(
            Flash(sample_point, color="#00BF00")
        )
        self.wait(2)

        texel_centers = []
        texel_center_group = Group()
        for iy in range(3):
            row = []
            for ix in range(4):
                texel_center = Circle(radius=0.05).set_fill("#000000", opacity=1).set_stroke(opacity=0).move_to((-3 + 1.5 * (ix + 0.5), 2.75 - 1.5 * (iy + 0.5), 0))
                row.append(texel_center)
                texel_center_group.add(texel_center)
            texel_centers.append(row)
        self.play(
            *self.swap_caption("The first thing we will do is put a dot in the middle of every texel.")
        )
        self.play(
            *[Write(j) for j in texel_center_group]
        )
        self.wait(2)

        self.play(
            *self.swap_caption("When sampling the color at some point, we only care about the four texel centers surrounding that point.")
        )
        self.wait(0.5)

        surrounding_square = Group(
            *[Line(texel_centers[1 < j][0 < j < 3], texel_centers[0 < j < 3][j < 2]) for j in range(4)]
        )
        for i in surrounding_square:
            i.z_index = 5
        self.play(
            *[Create(j) for j in surrounding_square],
            run_time=0.5
        )

        # Crop texture
        cropped_texture = ImageMobject(self.get_asset("4x3_texture_cropped.png")).scale_to_fit_width(1.5).move_to(surrounding_square)
        corner_group = Group(texel_centers[0][0], texel_centers[0][1], texel_centers[1][0], texel_centers[1][1])
        self.add(cropped_texture)
        self.add(sample_point)
        self.add(corner_group)
        self.play(
            FadeOut(nearest_neighbor_texture),
            FadeOut(Group(*texel_center_group).remove(*corner_group))
        )
        self.wait(0.4)

        # Zoom in
        to_zoom_group = Group(cropped_texture, sample_point, *corner_group, *surrounding_square)
        to_zoom_group.generate_target()
        to_zoom_group.target.move_to(ORIGIN)
        to_zoom_group.target.scale(3)
        to_zoom_group.target.shift((3, 1, 0))
        self.play(
            MoveToTarget(to_zoom_group)
        )
        self.wait(2)

        weight_formulas = [
            Tex("$Color = w_1 \cdot$"),
            Tex("$+ \, w_2 \cdot$"),
            Tex("$+ \, w_3 \cdot$"),
            Tex("$+ \, w_4 \cdot$"),
        ]
        weight_formula_group = Group(*weight_formulas)
        weight_formula_group.arrange(DOWN)
        for i in range(1, 4):
            weight_formula_group[i].align_to(weight_formula_group[0], RIGHT)
        for i in range(4):
            square = Square(side_length=0.32, color="#BFBFBF", fill_opacity=1).set_fill(COLORS[[2, 3, 0, 1][i]]).next_to(weight_formulas[i], RIGHT, buff=0.2)
            weight_formula_group.add(square)
        weight_formula_group.move_to((-3.5, 0, 0))
        self.play(
            FadeIn(weight_formula_group, shift=RIGHT),
            *self.swap_caption("The color at our sample point will be some weighted average between the colors of these four texels.")
        )
        self.wait(4)

        # Draw distances
        distance_group = Group(
            Line().add_updater(
                lambda m, dt: m.put_start_and_end_on(
                    (sample_point.get_center()[0] - 0.15, sample_point.get_center()[1], 0),
                    (texel_centers[0][0].get_center()[0], sample_point.get_center()[1], 0)
                )
            ),
            Line().add_updater(
                lambda m, dt: m.put_start_and_end_on(
                    (sample_point.get_center()[0] + 0.15, sample_point.get_center()[1], 0),
                    (texel_centers[0][1].get_center()[0], sample_point.get_center()[1], 0)
                )
            ),
            Line().add_updater(
                lambda m, dt: m.put_start_and_end_on(
                    (sample_point.get_center()[0], sample_point.get_center()[1] + 0.15, 0),
                    (sample_point.get_center()[0], texel_centers[0][0].get_center()[1], 0)
                )
            ),
            Line().add_updater(
                lambda m, dt: m.put_start_and_end_on(
                    (sample_point.get_center()[0], sample_point.get_center()[1] - 0.15, 0),
                    (sample_point.get_center()[0], texel_centers[1][0].get_center()[1], 0)
                )
            )
        )
        self.play(
            *self.swap_caption("These weights are decided by the proximity of our point to each of the texel centers.")
        )
        for i in distance_group:
            i.z_index = 5
            i.set_color("#FFFFFF")
        self.play(
            *[Create(j) for j in distance_group],
            run_time=0.5
        )
        self.wait(3)

        # Draw rectangles
        area_label_group = Group(
            *[Tex(f"$w_{[2, 1, 4, 3][j]}$").set_color(average_color(COLORS[3 - j], "#FFFFFF")) for j in range(4)]
        )
        def rectangle_updater(rectangle, index):
            texel_center = corner_group[index].get_center()
            sample_point_center = sample_point.get_center()
            position = (sample_point_center + texel_center) / 2
            size = np.abs(sample_point_center - texel_center)
            rectangle.stretch_to_fit_width(size[0])
            rectangle.stretch_to_fit_height(size[1])
            rectangle.move_to(position)
            area_label_group[index].move_to(position)
        rectangle_group = Group(
            Rectangle().set_fill(COLORS[3], opacity=0.8).add_updater(lambda m, dt: rectangle_updater(m, 0)),
            Rectangle().set_fill(COLORS[2], opacity=0.8).add_updater(lambda m, dt: rectangle_updater(m, 1)),
            Rectangle().set_fill(COLORS[1], opacity=0.8).add_updater(lambda m, dt: rectangle_updater(m, 2)),
            Rectangle().set_fill(COLORS[0], opacity=0.8).add_updater(lambda m, dt: rectangle_updater(m, 3))
        )
        for i in range(4):
            area_label_group[i].move_to((corner_group[i].get_center() + sample_point.get_center()) / 2)
        self.play(
            *self.swap_caption("More specifically, the weight of a certain texel depends on the area of the rectangle opposing it.")
        )
        self.add_foreground_mobjects(*corner_group, sample_point)
        self.play(
            FadeIn(rectangle_group),
            FadeIn(area_label_group),
            *[corner_group[j].animate.set_color(COLORS[j]).set_stroke("#FFFFFF", opacity=1) for j in range(4)],
            sample_point.animate.set_stroke("#FFFFFF", opacity=1)
        )
        self.remove_foreground_mobjects(*corner_group, sample_point)
        self.wait(3)

        # Move around sample point
        self.play(
            *self.swap_caption("This makes sense, since the closer the sample point is to this texel, the bigger the opposing area is, and vice versa.")
        )
        self.wait(0.6)
        self.play(
            sample_point.animate.shift((2, 0, 0)),
            run_time=0.6
        )
        self.wait(0.6)
        self.play(
            sample_point.animate.shift((-1.2, 1.6, 0)),
            run_time=0.6
        )
        self.wait(1.6)
        
        # Move close to yellow
        self.play(
            sample_point.animate.shift((-1.6, 0.8, 0)),
            *self.swap_caption("As an example, if the sample point is close to the yellow texel, we will get a lot of yellow at our sample point.", t2c={"yellow": COLORS[0]})
        )
        self.wait(4.5)

        # Write α, 1 - α, β and 1 - β
        self.play(
            *self.swap_caption("To formalize this, we can describe the horizontal and vertical position of our point between the texel centers with α and β respectively, both ranging from 0 to 1.", t2c={"α": "#FFFF00", "β": "#FF1F0F"}),
            sample_point.animate.shift((0.8, -2.4, 0))
        )
        
        distance_label_group = Group(
            MathTex("\\alpha", substrings_to_isolate=["\\alpha", "\\beta"]).scale(0.6).add_updater(lambda m, dt: m.next_to(distance_group[0].get_center(), UP, buff=0.1)),
            MathTex("1 - \\alpha", substrings_to_isolate=["\\alpha", "\\beta"]).scale(0.6).add_updater(lambda m, dt: m.next_to(distance_group[1].get_center(), UP, buff=0.1)),
            MathTex("1 - \\beta", substrings_to_isolate=["\\alpha", "\\beta"]).scale(0.6).add_updater(lambda m, dt: m.next_to(distance_group[2].get_center(), RIGHT, buff=0.1)),
            MathTex("\\beta", substrings_to_isolate=["\\alpha", "\\beta"]).scale(0.6).add_updater(lambda m, dt: m.next_to(distance_group[3].get_center(), RIGHT, buff=0.1)),
        )
        for i in distance_label_group:
            i.set_color_by_tex("\\alpha", "#FFFF00")
            i.set_color_by_tex("\\beta", "#FF1F0F")
        self.play(
            *[Write(j) for j in distance_label_group]
        )
        self.wait(4.5)

        self.play(
            *self.swap_caption("All of the four rectangular areas can be expressed in just α and β.", t2c={"α": "#FFFF00", "β": "#FF1F0F"})
        )
        self.wait(3.5)

        # Rewrite formula
        new_weight_formulas = [
            MathTex("Color = (1 - \\alpha) \cdot (1 - \\beta) \cdot", substrings_to_isolate=["\\alpha", "\\beta"]),
            MathTex("+ \, \\alpha \cdot (1 - \\beta) \cdot", substrings_to_isolate=["\\alpha", "\\beta"]),
            MathTex("+ \, (1 - \\alpha) \cdot \\beta \cdot", substrings_to_isolate=["\\alpha", "\\beta"]),
            MathTex("+ \, \\alpha \cdot \\beta \cdot", substrings_to_isolate=["\\alpha", "\\beta"])
        ]
        for i in new_weight_formulas:
            i.set_color_by_tex("\\alpha", "#FFFF00")
            i.set_color_by_tex("\\beta", "#FF1F0F")
        new_weight_formula_group = Group(*new_weight_formulas)
        new_weight_formula_group.arrange(DOWN)
        for i in range(1, 4):
            new_weight_formula_group[i].align_to(new_weight_formula_group[0], RIGHT)
        new_weight_formula_group.move_to((-3.5, 0, 0))
        self.play(
            *self.swap_caption("This means our entire formula be expressed in just four colors and two variables.")
        )
        self.play(
            *[ReplacementTransform(weight_formulas[j], new_weight_formulas[j]) for j in range(4)],
            *[weight_formula_group[j + 4].animate.next_to(new_weight_formulas[j], RIGHT, buff=0.2) for j in range(4)],
        )
        self.wait(3)

        self.play(
            *self.swap_caption("What we see here, is the formula that computers often use to apply bilinear interpolation.")
        )
        self.wait(4)

        stack = []
        for iy in range(16):
            for ix in range(16):
                stack.append((ix, iy))
        random.shuffle(stack)
        
        dot_group = Group()
        while stack:
            ix, iy = stack.pop()
            alpha = (ix + 0.5) / 16
            beta = (iy + 0.5) / 16

            color = interpolate_color(interpolate_color(COLORS[0], COLORS[1], alpha), interpolate_color(COLORS[2], COLORS[3], alpha), beta)
            corner_pos = [j.get_center() for j in corner_group]
            position = ((1 - alpha) * corner_pos[0] + alpha * corner_pos[1]) * (1 - beta) + ((1 - alpha) * corner_pos[2] + alpha * corner_pos[3]) * beta

            square = Square(0.3).set_stroke(opacity=0).set_fill(color, opacity=1).move_to(position)
            square.z_index = 75
            dot_group.add(square)
        
        self.play(
            *self.swap_caption("If we apply this formula to a bunch of points, we get a nice gradient."),
            FadeOut(rectangle_group),
            FadeOut(area_label_group),
            FadeOut(distance_group),
            FadeOut(distance_label_group),
            FadeOut(sample_point),
            FadeOut(corner_group),
            FadeOut(surrounding_square)
        )
        self.play(
            AnimationGroup(
                *[GrowFromCenter(j) for j in dot_group],
                lag_ratio=0.008
            )
        )
        self.wait(3)

        dot_group.generate_target()
        dot_group.target.scale(1 / 3)
        dot_group.target.move_to((-1.47, 1.22, 0))
        self.remove(cropped_texture)
        self.play(
            FadeOut(weight_formula_group),
            FadeOut(new_weight_formula_group),
            FadeIn(nearest_neighbor_texture),
            MoveToTarget(dot_group),
            *self.swap_caption("When we apply this function to every pixel on screen that is in between four texels, we get a nice and smooth image.")
        )
        inner_rectangle = Rectangle("#FFFFFF", 3, 4.5).shift((0, 0.5, 0))
        self.play(
            FadeIn(interpolated_inner_texture),
            FadeIn(bilinear_interpolation_text, shift=RIGHT),
            Create(inner_rectangle)
        )
        self.play(
            FadeOut(dot_group),
            run_time=0.3
        )
        self.wait(3)

        self.play(
            *self.swap_caption("This looks nice, but what do we do about the edges?")
        )
        self.wait(3)

        texel_center_all_group = Group()
        texel_center_edge_group = Group()
        for iy in range(-1, 4):
            for ix in range(-1, 5):
                in_center = 0 <= iy <= 2 and 0 <= ix <= 3
                texel_center = Circle(radius=0.05).set_fill("#000000" if in_center else "#FFFFFF", opacity=1).set_stroke(opacity=0).move_to((-3 + 1.5 * (ix + 0.5), 2.75 - 1.5 * (iy + 0.5), 0))
                texel_center_all_group.add(texel_center)
                if not in_center:
                    texel_center_edge_group.add(texel_center)
        self.play(
            *self.swap_caption("Since the outer texel centers do not have a color assigned to them yet, we'll have to extend the texture somehow."),
            *[Write(j) for j in texel_center_all_group]
        )
        self.wait(0.5)
        self.play(
            *[Flash(j, color="#FFFFFF") for j in texel_center_edge_group]
        )
        self.wait(3)

        self.play(
            *self.swap_caption("This can be done by repeating or clamping the texture.", t2c = {"repeating": "#FFFF00", "clamping": "#FFFF00"}),
            FadeOut(texel_center_all_group)
        )
        self.wait(0.4)

        bilinear_interpolation_repeat_text = Tex("Interpolated (Repeated)").scale(0.6).set_opacity(0.5).next_to(nearest_neighbor_texture, UP)
        self.play(
            FadeOut(bilinear_interpolation_text, shift=RIGHT),
            FadeIn(bilinear_interpolation_repeat_text, shift=RIGHT),
            FadeIn(interpolated_repeat_texture)
        )
        self.wait(2.4)

        bilinear_interpolation_clamp_text = Tex("Interpolated (Clamped)").scale(0.6).set_opacity(0.5).next_to(nearest_neighbor_texture, UP)
        self.play(
            FadeOut(bilinear_interpolation_repeat_text, shift=RIGHT),
            FadeIn(bilinear_interpolation_clamp_text, shift=RIGHT),
            FadeIn(interpolated_clamp_texture)
        )
        self.wait(2)

        self.play(
            *self.swap_caption("Whichever method is used depends on the programmer's implementation.")
        )
        self.wait(2)

HIGH_QUALITY = False
START_AT = 0
END_AT = 1000

if __name__ == "__main__":
    render_video(os.path.realpath(__file__), HIGH_QUALITY, START_AT, END_AT)