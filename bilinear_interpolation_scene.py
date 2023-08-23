from imports import *
from manim import *
import random

random.seed(4136121025)

class MainScene(CGScene):
    def get_title(self):
        return "Bilinear Interpolation"

    def animate(self):
        mona_lisa_original_texture = ImageMobject(self.get_asset("mona_lisa_small.png"))
        mona_lisa_original_texture.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        mona_lisa_detailed_texture = ImageMobject(self.get_asset("mona_lisa_big.png"))
        mona_lisa_detailed_texture.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])

        self.play(
            *self.swap_caption(
                "Here we have a beautiful copy of the Mona Lisa."
            ),
            FadeIn(mona_lisa_original_texture, shift=DOWN)
        )
        self.wait(2.5)

        self.play(
            *self.swap_caption(
                "Except, this Mona Lisa lacks a little in detail. We can count the texels when we're up close!"
            ),
        )
        self.play(
            mona_lisa_original_texture.animate.scale(7.5, about_point=(0, 0.3, 0)),
            run_time=1.2
        )
        self.wait(3.5)
        
        self.play(
            *self.swap_caption(
                "Visible texels can ruin the observer's immersion, so we would like to hide them somehow.",
                t2c={"hide": "#FFFF00"}
            ),
        )
        self.wait(4)
        
        mona_lisa_detailed_texture.match_height(mona_lisa_original_texture).move_to(mona_lisa_original_texture)
        self.play(
            *self.swap_caption(
                "Using a more detailed picture would help, but only to a certain extent, and it would require a lot more memory.",
            ),
            FadeIn(mona_lisa_detailed_texture)
        )
        self.wait(3.2)
        self.play(
            FadeOut(mona_lisa_detailed_texture)
        )
        self.wait(0.3)

        self.play(
            *self.swap_caption(
                "Instead, we will try to smoothen the texels using a technique called bilinear interpolation.",
                t2c={"bilinear": "#FFFF00", "interpolation": "#FFFF00"}
            ),
        )

        mona_lisa_interpolated_texture = mona_lisa_original_texture.copy()
        mona_lisa_interpolated_texture.set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        self.add_foreground_mobject(mona_lisa_original_texture)
        original_text = Tex("Original").set_opacity(0.5)
        original_text.scale(0.6).next_to(mona_lisa_original_texture, UP).shift((-3.2, 0, 0))
        interpolated_text = Tex("Interpolated").set_opacity(0.5)
        interpolated_text.scale(0.6).next_to(mona_lisa_original_texture, UP).shift((3.2, 0, 0))
        self.play(
            mona_lisa_interpolated_texture.animate.shift((3.2, 0, 0)),
            mona_lisa_original_texture.animate.shift((-3.2, 0, 0)),
            FadeIn(original_text),
            FadeIn(interpolated_text),
            run_time=0.8
        )
        self.wait(3.5)
        
        self.play(
            *self.swap_caption(
                "So how does it work?",
            ),
        )
        self.wait(0.5)

        self.play(
            FadeOut(mona_lisa_original_texture),
            FadeOut(mona_lisa_interpolated_texture),
            FadeOut(original_text),
            FadeOut(interpolated_text),
            run_time=0.8
        )
    
        COLORS = [
            ["#EDAE49", "#D1495B", "#D17C5B", "#EDAE49"],
            ["#30638E", "#003D5B", "#A01347", "#D1495B"],
            ["#00798C", "#30638E", "#00798C", "#803D93"],
        ]
        nearest_neighbor_texture = Group()
        for iy in range(3):
            for ix in range(4):
                square = Square(1.5).set_stroke(opacity=0).set_fill(COLORS[iy][ix], opacity=1)
                square.move_to((ix * 1.5, -iy * 1.5, 0))
                nearest_neighbor_texture.add(square)
        nearest_neighbor_texture.move_to((0, 0.5, 0))

        interpolated_clamp_texture = ImageMobject(self.get_asset("4x3_texture_interpolated_clamp.png")).scale_to_fit_width(6).move_to(nearest_neighbor_texture)
        interpolated_repeat_texture = ImageMobject(self.get_asset("4x3_texture_interpolated_repeat.png")).scale_to_fit_width(6).move_to(nearest_neighbor_texture)
        interpolated_inner_texture = ImageMobject(self.get_asset("4x3_texture_interpolated_inner.png")).scale_to_fit_width(4.5).move_to(nearest_neighbor_texture)

        # Show 4x3 texture
        self.play(
            AnimationGroup(
                *[FadeIn(j, shift=UP) for j in nearest_neighbor_texture],
                lag_ratio=0.08,
            )
        )

        self.play(
            *self.swap_caption(
                "Here we have a small texture where the edges between the texels are very visible."
            ),
        )

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
            *create_actions,
            run_time=0.8
        )
        self.wait(3)

        self.play(
            *self.swap_caption(
                "Using bilinear interpolation, we'll make this color-to-color transition smoother."
            ),
            *fade_out_actions,
        )
        self.wait(3.5)

        X = 0.75
        Y = 1.3

        self.play(
            *self.swap_caption(
                "Suppose we try to sample the color from the texture at this point."
            ),
        )
        self.wait(1)

        # Place point, draw attention to it
        sample_point = Circle(radius=0.05).set_fill("#FFFFFF", opacity=1).set_stroke("#FFFFFF", opacity=1).move_to((-3 + 1.5 * X, 2.75 - 1.5 * Y, 0))
        sample_point.z_index = 15
        self.play(
            FadeIn(sample_point, scale=7),
            run_time=0.6
        )
        self.wait(0.2)
        self.play(
            Flash(sample_point, color="#FFFFFF")
        )
        self.wait(2)

        texel_centers = []
        texel_center_group = Group()
        for iy in range(3):
            row = []
            for ix in range(4):
                texel_center = Circle(radius=0.05).set_fill("#FFFFFF", opacity=1).set_stroke("#FFFFFF", opacity=1).move_to((-3 + 1.5 * (ix + 0.5), 2.75 - 1.5 * (iy + 0.5), 0))
                row.append(texel_center)
                texel_center_group.add(texel_center)
            texel_centers.append(row)
        self.play(
            *self.swap_caption(
                "The first thing we will do is represent each texel as a dot in its center."
            )
        )
        self.play(
            *[FadeIn(j, scale=3) for j in texel_center_group]
        )
        self.wait(2)

        self.play(
            *self.swap_caption(
                "When sampling the color at some point, we only care about the four dots surrounding that point."
            )
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
        cropped_texture = Group()
        for iy in range(2):
            for ix in range(2):
                square = Square(0.75).set_stroke(opacity=0).set_fill(COLORS[iy][ix], opacity=1)
                square.move_to((ix * 0.75, -iy * 0.75, 0))
                cropped_texture.add(square)
        cropped_texture.move_to(surrounding_square)
        corner_group = Group(texel_centers[0][0], texel_centers[0][1], texel_centers[1][0], texel_centers[1][1])
        for obj in corner_group:
            obj.z_index = 10

        self.add(cropped_texture)
        self.add(sample_point)
        self.add(corner_group)
        self.play(
            *[j.animate.set_fill(opacity=0.5) for j in nearest_neighbor_texture],
            FadeOut(Group(*texel_center_group).remove(*corner_group))
        )
        self.wait(0.4)

        # Zoom in
        to_zoom_group = Group(*nearest_neighbor_texture, cropped_texture, sample_point, *corner_group, *surrounding_square)
        zoom_center = cropped_texture.get_center()
        for obj in to_zoom_group:
            obj.generate_target()
            obj.target.shift(-zoom_center)
            obj.target.scale(3, about_point=ORIGIN)
            obj.target.shift((3, 0.9, 0))
        sample_point.target.set_fill("#000000")
        for iy in range(2):
            for ix in range(2):
                corner_group[2 * iy + ix].target.set_fill(COLORS[iy][ix])
        self.play(
            *[MoveToTarget(j) for j in to_zoom_group]
        )
        self.wait(2)

        weight_formulas = [
            Tex("$= w_1 \cdot$").set_background_stroke(color=BACKGROUND_COLOR, width=3),
            Tex("$+ \, w_2 \cdot$").set_background_stroke(color=BACKGROUND_COLOR, width=3),
            Tex("$+ \, w_3 \cdot$").set_background_stroke(color=BACKGROUND_COLOR, width=3),
            Tex("$+ \, w_4 \cdot$").set_background_stroke(color=BACKGROUND_COLOR, width=3),
        ]
        weight_formula_group = Group(*weight_formulas)
        weight_formula_group.arrange(DOWN)
        for i in range(1, 4):
            weight_formula_group[i].align_to(weight_formula_group[0], RIGHT)
        weight_formula_group.move_to((-3.8, 0.5, 0))

        result_formula_square = Square(side_length=0.64, color="#FFFFFF", fill_opacity=1).set_fill("#000000")
        result_formula_square.next_to(weight_formulas[0], LEFT, buff=0.2).shift(UP * 0.05)
        color_formula_group = Group()
        for i in range(4):
            square = Square(side_length=0.32, color="#FFFFFF", fill_opacity=1).set_fill(COLORS[1 - i // 2][i % 2])
            square.next_to(weight_formulas[i], RIGHT, buff=0.2).shift(UP * 0.03)
            color_formula_group.add(square)
        self.play(
            *self.swap_caption(
                "The color at our sample point will be some weighted average between the colors of these four texels."
            ),
            FadeIn(result_formula_square, shift=RIGHT),
            FadeIn(weight_formula_group, shift=RIGHT),
            FadeIn(color_formula_group, shift=RIGHT),
        )
        self.wait(4)

        # Draw distances
        distance_group = Group(
            Line().add_updater(
                lambda m, dt: m.put_start_and_end_on(
                    (sample_point.get_left()[0], sample_point.get_y(), 0),
                    (texel_centers[0][0].get_x(), sample_point.get_y(), 0)
                )
            ),
            Line().add_updater(
                lambda m, dt: m.put_start_and_end_on(
                    (sample_point.get_right()[0], sample_point.get_y(), 0),
                    (texel_centers[0][1].get_x(), sample_point.get_y(), 0)
                )
            ),
            Line().add_updater(
                lambda m, dt: m.put_start_and_end_on(
                    (sample_point.get_x(), sample_point.get_top()[1], 0),
                    (sample_point.get_x(), texel_centers[0][0].get_y(), 0)
                )
            ),
            Line().add_updater(
                lambda m, dt: m.put_start_and_end_on(
                    (sample_point.get_x(), sample_point.get_bottom()[1], 0),
                    (sample_point.get_x(), texel_centers[1][0].get_y(), 0)
                )
            )
        )
        self.play(
            *self.swap_caption(
                "These weights are decided by the proximity of our point to each of the texel centers."
            )
        )
        for i in distance_group:
            i.z_index = 5
            i.set_color("#FFFFFF")
        self.wait(4)

        # Draw rectangles
        rectangle_group = Group(*[Rectangle() for _ in range(4)])
        area_label_group = Group(
            *[
                Tex(f"$w_{[2, 1, 4, 3][j]}$").set_color(average_color(COLORS[1 - j // 2][1 - j % 2], "#FFFFFF")).set_background_stroke(color=BACKGROUND_COLOR, width=3)
                for j in range(4)
            ]
        )
        def rectangle_updater(idx):
            rectangle = rectangle_group[idx]
            texel_center = corner_group[idx].get_center()
            sample_point_center = sample_point.get_center()
            position = (sample_point_center + texel_center) / 2
            size = np.abs(sample_point_center - texel_center)
            rectangle.stretch_to_fit_width(max(size[0], 1e-3))
            rectangle.stretch_to_fit_height(max(size[1], 1e-3))
            rectangle.move_to(position)
            area_label_opacity = min(1, min(size[0], size[1]) * 2 - 0.1)
            area_label_group[idx].set_opacity(area_label_opacity).move_to(position)
        for i in range(4):
            rectangle = rectangle_group[i]
            rectangle.set_fill(COLORS[1 - i // 2][1 - i % 2], opacity=0.8)
            rectangle_updater(i)
        self.play(
            *self.swap_caption(
                "More specifically, the weight of a certain texel depends on the area of the rectangle opposing it.",
                t2c={"area": "#FFFF00"}
            ),
            *[Create(j) for j in distance_group],
        )
        self.wait(0.5)

        def move_rectangle_into_position(idx):
            rectangle = rectangle_group[idx]
            area_label = area_label_group[idx]
            corner = corner_group[3 - idx].get_center()

            rectangle.scale(0.001, about_point=corner)
            area_label.scale(0.001, about_point=corner)
            return [
                rectangle.animate.scale(1000, about_point=corner),
                area_label.animate.scale(1000, about_point=corner),
            ]

        def get_sample_point_color(mult=[1, 1, 1, 1], offset=(0, 0)):
            width = corner_group[3].get_x() - corner_group[2].get_x()
            height = corner_group[0].get_y() - corner_group[2].get_y()
            alpha = (sample_point.get_x() + offset[0] - corner_group[2].get_x()) / width
            beta = (sample_point.get_y() + offset[1] - corner_group[2].get_y()) / height

            return rgb_to_color(
                    color_to_rgb(COLORS[0][0]) * (1 - alpha) * beta * mult[0] \
                    + color_to_rgb(COLORS[0][1]) * alpha * beta * mult[1] \
                    + color_to_rgb(COLORS[1][0]) * (1 - alpha) * (1 - beta) * mult[2] \
                    + color_to_rgb(COLORS[1][1]) * alpha * (1 - beta) * mult[3]
                )

        # Introduce first color
        self.add_foreground_mobjects(*corner_group, sample_point)
        self.play(
            *move_rectangle_into_position(1),
            run_time=1.2
        )
        self.wait(0.5)

        rectangle_group[1].add_updater(lambda m: rectangle_updater(1))
        self.play(
            sample_point.animate.scale(2),
            run_time=0.8
        )
        self.wait(0.2)
        color = get_sample_point_color([0, 0, 1, 0])
        self.play(
            sample_point.animate.set_fill(color),
            result_formula_square.animate.set_fill(color),
            run_time=0.6
        )
        self.wait(1.5)

        # Move around sample point
        self.play(
            *self.swap_caption(
                "The closer the sample point is to a corner, the bigger its opposing rectangle, the higher its weight, and the more dominant the color becomes."
            )
        )
        self.wait(0.5)
        color = get_sample_point_color([0, 0, 1, 0], (-0.5, -0.4))
        self.play(
            sample_point.animate.shift((-0.5, -0.4, 0)).set_fill(color),
            result_formula_square.animate.set_fill(color),
            run_time=1
        )
        self.wait(2)
        color = get_sample_point_color([0, 0, 1, 0], (2, 3))
        self.play(
            sample_point.animate.shift((2, 3, 0)).set_fill(color),
            result_formula_square.animate.set_fill(color),
            run_time=1
        )
        self.wait(2)

        # Introduce other colors
        for i in [0, 2, 3]:
            rectangle_updater(i)

        self.play(
            *self.swap_caption(
                "We similarly calculate the other weights, and take the weighted average as our final color."
            )
        )

        color = get_sample_point_color([0, 0, 1, 1])
        self.play(
            *move_rectangle_into_position(0),
            sample_point.animate.set_fill(color),
            result_formula_square.animate.set_fill(color),
            run_time=0.8
        )
        rectangle_group[0].add_updater(lambda m: rectangle_updater(0))
        color = get_sample_point_color([1, 0, 1, 1])
        self.play(
            *move_rectangle_into_position(3),
            sample_point.animate.set_fill(color),
            result_formula_square.animate.set_fill(color),
            run_time=0.8
        )
        rectangle_group[3].add_updater(lambda m: rectangle_updater(3))
        color = get_sample_point_color([1, 1, 1, 1])
        self.play(
            *move_rectangle_into_position(2),
            sample_point.animate.set_fill(color),
            result_formula_square.animate.set_fill(color),
            run_time=0.8
        )
        rectangle_group[2].add_updater(lambda m: rectangle_updater(2))
        self.remove_foreground_mobjects(*corner_group, sample_point)
        self.wait(3)

        # Move around sample point
        self.wait(0.6)
        color = get_sample_point_color([1, 1, 1, 1], (1, -2))
        self.play(
            sample_point.animate.shift((1, -2, 0)).set_fill(color),
            result_formula_square.animate.set_fill(color),
            run_time=1.6
        )
        self.wait(1.6)

        # Move close to yellow
        color = get_sample_point_color([1, 1, 1, 1], (-2.6, 2.6))
        self.play(
            sample_point.animate.shift((-2.6, 2.6, 0)).set_fill(color),
            result_formula_square.animate.set_fill(color),
            *self.swap_caption(
                "Note that if the sample point is close to the yellow corner, we will get a very yellow-like sample back.",
                t2c={"yellow": COLORS[0][0]}
            )
        )
        self.wait(4.5)

        # Move on top of yellow
        color = get_sample_point_color([1, 1, 1, 1], (-1, 0.4))
        self.play(
            sample_point.animate.shift((-1, 0.4, 0)).set_fill(color),
            result_formula_square.animate.set_fill(color),
            *self.swap_caption(
                "If the point lies directly on top of the corner, the sample will be completely yellow.",
                t2c={"yellow": COLORS[0][0]},
                t2s={"completely": ITALIC}
            )
        )
        self.wait(4.5)

        # Write α, 1 - α, β and 1 - β
        color = get_sample_point_color([1, 1, 1, 1], (1.6, -3.2))
        self.play(
            *self.swap_caption(
                "To calculate the areas, we can describe our sample point using the coordinates (α, β), between (0, 0) and (1, 1).",
                t2c={"α": "#FFFF00", "β": "#FF1F0F"}
            ),
            sample_point.animate.shift((1.6, -3.2, 0)).set_fill(color),
            result_formula_square.animate.set_fill(color),
        )
        self.wait(0.5)

        zero_zero_label = Tex("$(0, 0)$").set_background_stroke(color=BACKGROUND_COLOR, width=3).scale(0.8).move_to(corner_group[2].get_center() + np.array([0, -0.4, 0]))
        one_one_label = Tex("$(1, 1)$").set_background_stroke(color=BACKGROUND_COLOR, width=3).scale(0.8).move_to(corner_group[1].get_center() + np.array([0, 0.4, 0]))
        alpha_beta_label = MathTex("(\\alpha, \\beta)", substrings_to_isolate=["\\alpha", "\\beta"]).set_background_stroke(color=BACKGROUND_COLOR, width=3).scale(0.8).move_to(sample_point.get_center() + np.array([0.6, 0.5, 0]))
        alpha_beta_label.z_index = 100
        distance_label_group = Group(
            MathTex("\\alpha", substrings_to_isolate=["\\alpha", "\\beta"]).set_background_stroke(color=BACKGROUND_COLOR, width=3).scale(0.6).next_to(distance_group[0].get_center(), UP, buff=0.1),
            MathTex("1 - \\alpha", substrings_to_isolate=["\\alpha", "\\beta"]).set_background_stroke(color=BACKGROUND_COLOR, width=3).scale(0.6).next_to(distance_group[1].get_center(), UP, buff=0.1),
            MathTex("1 - \\beta", substrings_to_isolate=["\\alpha", "\\beta"]).set_background_stroke(color=BACKGROUND_COLOR, width=3).scale(0.6).next_to(distance_group[2].get_center(), RIGHT, buff=0.1),
            MathTex("\\beta", substrings_to_isolate=["\\alpha", "\\beta"]).set_background_stroke(color=BACKGROUND_COLOR, width=3).scale(0.6).next_to(distance_group[3].get_center(), RIGHT, buff=0.1),
        )
        for i in [alpha_beta_label, *distance_label_group]:
            i.set_color_by_tex("\\alpha", "#FFFF00")
            i.set_color_by_tex("\\beta", "#FF1F0F")
        self.play(
            Write(zero_zero_label),
            Write(one_one_label),
            Write(alpha_beta_label),
            run_time=1.5
        )
        self.wait(3.5)

        self.play(
            *self.swap_caption(
                "The sides of the four rectangles can now be expressed in α and β.", t2c={"α": "#FFFF00", "β": "#FF1F0F"}
            )
        )
        self.wait(0.5)

        self.play(
            *[Write(j) for j in distance_label_group],
            run_time=1.5
        )
        self.wait(2.5)

        # Rewrite formula
        new_weight_formulas = [
            MathTex("= (1 - \\alpha) \cdot (1 - \\beta) \cdot", substrings_to_isolate=["\\alpha", "\\beta"]).set_background_stroke(color=BACKGROUND_COLOR, width=3),
            MathTex("+ \, \\alpha \cdot (1 - \\beta) \cdot", substrings_to_isolate=["\\alpha", "\\beta"]).set_background_stroke(color=BACKGROUND_COLOR, width=3),
            MathTex("+ \, (1 - \\alpha) \cdot \\beta \cdot", substrings_to_isolate=["\\alpha", "\\beta"]).set_background_stroke(color=BACKGROUND_COLOR, width=3),
            MathTex("+ \, \\alpha \cdot \\beta \cdot", substrings_to_isolate=["\\alpha", "\\beta"]).set_background_stroke(color=BACKGROUND_COLOR, width=3)
        ]
        for i in new_weight_formulas:
            i.set_color_by_tex("\\alpha", "#FFFF00")
            i.set_color_by_tex("\\beta", "#FF1F0F")
        new_weight_formula_group = Group(*new_weight_formulas)
        new_weight_formula_group.arrange(DOWN)
        for i in range(1, 4):
            new_weight_formula_group[i].align_to(new_weight_formula_group[0], RIGHT)
        new_weight_formula_group.move_to((-3.2, 0.5, 0))
        self.play(
            *self.swap_caption(
                "Since area equals width times height, we can express our weights in α and β as well.",
                t2c={"α": "#FFFF00", "β": "#FF1F0F"}
            )
        )
        transform_actions = []
        for i in range(4):
            alpha_label = distance_label_group[1 - i % 2].copy()
            beta_label = distance_label_group[2 + i // 2].copy()
            self.add_foreground_mobjects(alpha_label, beta_label)

            action = AnimationGroup(
                alpha_label.animate.set_opacity(0).move_to(new_weight_formulas[i]),
                beta_label.animate.set_opacity(0).move_to(new_weight_formulas[i]),
                ReplacementTransform(weight_formulas[i], new_weight_formulas[i]),
                *[result_formula_square.animate.next_to(new_weight_formulas[0], LEFT, buff=0.2).shift(UP * 0.02)] * (i == 0),
                color_formula_group[i].animate.next_to(new_weight_formulas[i], RIGHT, buff=0.2).shift(UP * 0.01),
            )
            transform_actions.append(action)
        self.play(
            AnimationGroup(
                *transform_actions,
                lag_ratio=0.6
            )
        )
        self.wait(3)

        self.play(
            *self.swap_caption(
                "What we see here, is the formula that computers often use to apply bilinear interpolation."
            )
        )
        self.wait(4)

        stack = []
        for iy in range(16):
            for ix in range(16):
                stack.append((ix, iy))
        random.shuffle(stack)

        pixel_group = Group()
        while stack:
            ix, iy = stack.pop()
            alpha = (ix + 0.5) / 16
            beta = (iy + 0.5) / 16

            color = interpolate_color(interpolate_color(COLORS[0][0], COLORS[0][1], alpha), interpolate_color(COLORS[1][0], COLORS[1][1], alpha), beta)
            corner_pos = [j.get_center() for j in corner_group]
            position = ((1 - alpha) * corner_pos[0] + alpha * corner_pos[1]) * (1 - beta) + ((1 - alpha) * corner_pos[2] + alpha * corner_pos[3]) * beta

            square = Square(0.3).set_stroke(opacity=0).set_fill(color, opacity=1).move_to(position)
            square.z_index = 75
            pixel_group.add(square)

        mask_rectangle = Rectangle(BACKGROUND_COLOR, 1, 1.5).shift((-7.05, 1.65, 0)).set_stroke(opacity=0).set_fill(opacity=1)
        self.add(mask_rectangle)
        self.add_foreground_mobject(mask_rectangle)
        self.play(
            *self.swap_caption(
                "If we apply this formula to a bunch of points, we get a nice gradient square."
            ),
            FadeOut(rectangle_group),
            FadeOut(area_label_group),
            FadeOut(distance_group),
            FadeOut(distance_label_group),
            FadeOut(sample_point),
            FadeOut(corner_group),
            FadeOut(surrounding_square),
            FadeOut(zero_zero_label),
            FadeOut(one_one_label),
            FadeOut(alpha_beta_label),
            result_formula_square.animate.shift(LEFT * 1.5),
            new_weight_formula_group.animate.shift(LEFT * 1.5),
            color_formula_group.animate.shift(LEFT * 1.5),
            FadeIn(mask_rectangle, shift = LEFT * 1.5),
        )
        self.wait(0.5)
        self.play(
            AnimationGroup(
                *[GrowFromCenter(j) for j in pixel_group],
                lag_ratio=0.008
            )
        )
        self.wait(3)

        for obj in nearest_neighbor_texture:
            obj.set_fill(opacity=0.5)
            obj.generate_target()
            obj.target.shift((-3, -0.9, 0))
            obj.target.scale(1 / 3, about_point=ORIGIN)
            obj.target.shift(zoom_center)
            obj.target.set_fill(opacity=1)
        pixel_group.generate_target()
        pixel_group.target.shift((-3, -0.9, 0))
        pixel_group.target.scale(1 / 3, about_point=ORIGIN)
        pixel_group.target.shift(zoom_center)
        self.remove(cropped_texture)
        self.play(
            *self.swap_caption(
                "And after repeating the same process for each region in between texel centers, we end up with a smooth pattern."
            ),
            FadeOut(result_formula_square, shift=LEFT * 3),
            FadeOut(color_formula_group, shift=LEFT * 3),
            FadeOut(new_weight_formula_group, shift=LEFT * 3),
            mask_rectangle.animate.shift(LEFT * 3),
            *[MoveToTarget(j) for j in nearest_neighbor_texture],
            MoveToTarget(pixel_group),
        )
        self.wait(0.2)

        inner_rectangle = Rectangle("#FFFFFF", 3, 4.5).shift((0, 0.5, 0))
        inner_lines = Group(
            Line((-0.75, 2, 0), (-0.75, -1, 0)),
            Line((0.75, 2, 0), (0.75, -1, 0)),
            Line((-2.25, 0.5, 0), (2.25, 0.5, 0)),
        )
        texel_center_inner_group = Group()
        texel_center_edge_group = Group()
        for iy in range(-1, 4):
            for ix in range(-1, 5):
                in_center = 0 <= iy < 3 and 0 <= ix < 4
                texel_center = Circle(radius=0.05).set_fill("#FFFFFF", opacity=1).set_stroke(opacity=0).move_to((-3 + 1.5 * (ix + 0.5), 2.75 - 1.5 * (iy + 0.5), 0))
                if in_center:
                    texel_center_inner_group.add(texel_center)
                else:
                    texel_center_edge_group.add(texel_center)
        for obj in [inner_rectangle, *inner_lines, *texel_center_inner_group]:
            obj.z_index = 80


        # Show final version
        bilinear_interpolation_text = Tex("Interpolated").scale(0.6).set_opacity(0.5).next_to(nearest_neighbor_texture, UP)
        self.play(
            *[FadeIn(j, scale=3) for j in texel_center_inner_group],
            run_time=0.6
        )
        self.wait(0.2)
        self.play(
            Create(inner_rectangle),
            *[Create(j) for j in inner_lines]
        )
        self.wait(0.2)
        self.play(
            FadeIn(interpolated_inner_texture),
            FadeIn(bilinear_interpolation_text, shift=RIGHT),
            run_time=0.8
        )
        self.wait(0.2)
        self.play(
            FadeOut(pixel_group),
            FadeOut(inner_lines),
            run_time=0.3
        )
        self.wait(3)

        self.play(
            *self.swap_caption(
                "This looks good already, but what do we do about the edges?"
            )
        )
        self.wait(3)

        self.play(
            *self.swap_caption(
                "Since there are no extra texels around the image, we'll have to extend the texture ourselves somehow."
            ),
            *[FadeIn(j, scale=3) for j in texel_center_edge_group]
        )
        self.wait(0.5)
        self.play(
            *[Flash(j, color="#FFFFFF") for j in texel_center_edge_group]
        )
        self.wait(3)

        self.play(
            *self.swap_caption(
                "This can be done by clamping or repeating the texture.",
                t2c={"clamping": "#FFFF00", "repeating": "#FFFF00"}
            ),
            FadeOut(texel_center_inner_group),
            FadeOut(texel_center_edge_group),
            FadeOut(inner_rectangle),
        )
        self.wait(0.4)

        repeated_edges_fade_in_actions = []
        repeated_edges_fade_out_actions = []
        clamped_edges_fade_in_actions = []
        clamped_edges_fade_out_actions = []
        for iy in range(-1, 4):
            for ix in range(-1, 5):
                if 0 <= iy < 3 and 0 <= ix < 4:
                    continue

                direction = (DOWN * (iy == -1) + UP * (iy == 3) + RIGHT * (ix == -1) + LEFT * (ix == 4)) * 0.75

                repeated_rectangle = Rectangle("#FFFFFF", 0.75 * (1 + (0 <= iy < 3)), 0.75 * (1 + (0 <= ix < 4))).set_stroke(opacity=0)
                repeated_rectangle.move_to(nearest_neighbor_texture[0]).shift((1.5 * max(-0.75, min(ix, 3.75)), -1.5 * max(-0.75, min(iy, 2.75)), 0))
                repeated_rectangle.set_fill(COLORS[iy % 3][ix % 4], opacity=0.5)
                repeated_edges_fade_in_actions.append(FadeIn(repeated_rectangle, shift=direction))
                repeated_edges_fade_out_actions.append(FadeOut(repeated_rectangle))

                clamped_rectangle = repeated_rectangle.copy()
                clamped_rectangle.set_fill(COLORS[max(0, min(iy, 2))][max(0, min(ix, 3))])
                clamped_edges_fade_in_actions.append(FadeIn(clamped_rectangle, shift=-direction))
                clamped_edges_fade_out_actions.append(FadeOut(clamped_rectangle))
        
        bilinear_interpolation_clamp_text = Tex("Interpolated (Clamped)").set_opacity(0.5)
        bilinear_interpolation_clamp_text.scale(0.6).next_to(nearest_neighbor_texture, UP)
        bilinear_interpolation_clamp_text.z_index = 100
        self.play(
            FadeOut(bilinear_interpolation_text, shift=RIGHT),
            FadeIn(bilinear_interpolation_clamp_text, shift=RIGHT),
            *clamped_edges_fade_in_actions,
        )
        self.wait(0.6)
        self.play(
            FadeIn(interpolated_clamp_texture)
        )
        self.wait(0.4)
        self.play(
            *clamped_edges_fade_out_actions,
            run_time=0.8
        )
        self.wait(0.8)

        bilinear_interpolation_repeat_text = Tex("Interpolated (Repeated)").set_opacity(0.5)
        bilinear_interpolation_repeat_text.scale(0.6).next_to(nearest_neighbor_texture, UP)
        bilinear_interpolation_repeat_text.z_index = 100
        self.play(
            FadeOut(bilinear_interpolation_clamp_text, shift=RIGHT),
            FadeOut(interpolated_clamp_texture),
            FadeIn(bilinear_interpolation_repeat_text, shift=RIGHT),
            *repeated_edges_fade_in_actions,
        )
        self.wait(0.6)
        self.play(
            FadeIn(interpolated_repeat_texture)
        )
        self.wait(0.4)
        self.play(
            *repeated_edges_fade_out_actions,
            run_time=0.8
        )
        self.wait(0.8)

        self.play(
            *self.swap_caption(
                "Whichever method is used depends on the preference of the programmer or user."
            ),
        )
        self.wait(2)

HIGH_QUALITY = True
START_AT = 0
END_AT = 1000

if __name__ == "__main__":
    render_video(os.path.realpath(__file__), HIGH_QUALITY, START_AT, END_AT)