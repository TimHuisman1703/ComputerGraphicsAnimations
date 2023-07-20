from imports import *
from manim import *
from math import cos, pi, sin

class MainScene(CGScene):
    def get_title(self):
        return "Camera Projection"

    def animate(self):
        def cubify(point):
            factor = max([abs(j) for j in point])
            factor = pow(factor, 2 / 3)
            if factor < 1e-6:
                return point
            return point / factor
        
        def apply_transformation(matrix, point):
            vector = np.array([point[0], point[2], -point[1], 1])
            result = matrix @ vector
            return np.array([result[0] / result[3], -result[2] / result[3], result[1] / result[3]])
        
        self.play(
            *self.swap_caption(
                "When a camera takes a picture of a scene, each point in space is mapped to a pixel on screen.",
                t2c={"point in space": "#FFFF00", "pixel on screen": "#FFFF00"}
            )
        )
        self.wait(4)

        self.play(
            *self.swap_caption(
                "This conversion from 3D to 2D is done using three matrices.",
            )
        )

        # Show matrices
        matrix_group = Group(
            Matrix([
                ["k_x", "0", "0", "x_0"],
                ["0", "k_y", "0", "y_0"],
                ["0", "0", "1", "0"],
                ["0", "0", "0", "1"],
            ]),
            MobjectMatrix([
                [Tex("$\\frac{f}{aspect}$").scale(0.75), Tex("$0$"), Tex("$0$"), Tex("$0$")],
                [Tex("$0$"), Tex("$f$"), Tex("$0$"), Tex("$0$")],
                [Tex("$0$"), Tex("$0$"), Tex("$\\frac{near+far}{near-far}$").scale(0.45), Tex("$\\frac{2 \cdot near \cdot far}{near-far}$").scale(0.45)],
                [Tex("$0$"), Tex("$0$"), Tex("$-1$"), Tex("$0$")]
            ]),
            Matrix([
                ["m_{00}", "m_{01}", "m_{02}", "t_0"],
                ["m_{10}", "m_{11}", "m_{12}", "t_1"],
                ["m_{20}", "m_{21}", "m_{22}", "t_2"],
                ["0", "0", "0", "1"],
            ])
        ).arrange(RIGHT).scale(0.8).move_to(UP)
        matrix_group.add(
            Text("Image Matrix").set_color("#BFBFBF").scale(0.6).next_to(matrix_group[0], DOWN),
            Text("Projection Matrix").set_color("#BFBFBF").scale(0.6).next_to(matrix_group[1], DOWN),
            Text("Model View Matrix").set_color("#BFBFBF").scale(0.6).next_to(matrix_group[2], DOWN)
        )
        for obj in matrix_group:
            obj.z_index = 100
            self.add_fixed_in_frame_mobjects(obj)
        self.play(
            FadeIn(matrix_group)
        )
        self.wait(3.5)

        self.play(
            FadeOut(matrix_group),
            *self.swap_caption("Let's look at these operations one by one. Suppose we have a scene, and a camera observing it."),
        )

        # Create 3D scene
        object_group = Group(
            Sphere(radius=1).set_color("#00BF00"),
            Sphere(radius=0.9).set_color("#7F007F").shift((-0.7, -0.3, 0.9)),
            Sphere(radius=0.5).set_color("#FF0000").shift((0.9, 0.2, 0.5)),
            Sphere(radius=0.3).set_color("#007FFF").shift((0.7, 1.4, 0.3))
        )
        self.play(
            ApplyPointwiseFunction(
                lambda point: cubify(point),
                object_group[0]
            ),
            run_time=0
        )
        self.remove(object_group[0])
        object_group[0].scale(2).stretch(0.05, 2).shift(0.1 * IN)
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length = 6.5,
            y_length = 6.5,
            z_length = 6.5,
        )
        negative_x_label = Tex("$-x$").move_to(LEFT * 3.5)
        positive_x_label = Tex("$x$").move_to(RIGHT * 3.5)
        negative_y_label = Tex("$-y$").move_to(DOWN * 3.5)
        positive_y_label = Tex("$y$").move_to(UP * 3.5)
        negative_z_label = Tex("$-z$").move_to(IN * 3.5)
        positive_z_label = Tex("$z$").move_to(OUT * 3.5)
        axes_group = Group(
            axes,
            negative_x_label,
            positive_x_label,
            negative_y_label,
            positive_y_label,
            negative_z_label,
            positive_z_label
        )
        axes_group.rotate(pi / 2, RIGHT)

        # Camera/scene settings
        CAMERA_THETA = 130 * DEGREES
        CAMERA_PHI = -30 * DEGREES
        CAMERA_POSITION = np.array([sin(CAMERA_THETA) * sin(90 * DEGREES + CAMERA_PHI) * 4, -cos(CAMERA_THETA) * sin(90 * DEGREES + CAMERA_PHI) * 4, cos(90 * DEGREES + CAMERA_PHI) * 4])
        NEAR = 1
        FAR = 5
        F = 2
        ASPECT = 16 / 9

        # Normal points for frustrum
        points = [UP + (2 * (j < 2) - 1) * RIGHT * ASPECT / F + (2 * (0 < j < 3) - 1) * IN / F for j in range(4)]

        # Create and rotate camera and unit-cube group
        camera_group = Group(
            Sphere(radius=0.1).set_color("#7FFFFF"),
            *[Line(ORIGIN, 6 * points[j], stroke_width=2, color="#7FFFFF") for j in range(4)],
        )
        unit_cube_group = Group(
            *[Line(NEAR * points[j], FAR * points[j], stroke_width=2, color="#7FFFFF") for j in range(4)],
            *[Line(NEAR * points[j - 1], NEAR * points[j], stroke_width=2, color="#FFBF7F") for j in range(4)],
            *[Line(FAR * points[j - 1], FAR * points[j], stroke_width=2, color="#FF7FBF") for j in range(4)],
        )
        camera_group.rotate_about_origin(CAMERA_PHI, RIGHT).rotate_about_origin(CAMERA_THETA, OUT).shift(CAMERA_POSITION)
        unit_cube_group.rotate_about_origin(CAMERA_PHI, RIGHT).rotate_about_origin(CAMERA_THETA, OUT).shift(CAMERA_POSITION)

        # Show 3D scene
        self.set_camera_orientation(
            theta=-70 * DEGREES,
            phi=55 * DEGREES
        )
        self.play(
            *[Create(j) for j in axes_group],
            run_time = 1.2
        )
        self.play(
            FadeIn(object_group)
        )
        self.play(
            FadeIn(camera_group),
            FadeIn(unit_cube_group)
        )
        self.wait(3)

        # Move behind camera
        self.move_camera(
            theta=CAMERA_THETA - 90 * DEGREES,
            phi=90 * DEGREES + CAMERA_PHI,
            frame_center=-CAMERA_POSITION,
            added_anims=[
                *self.swap_caption("We want to take a picture from the camera's perspective."),
            ]
        )
        self.wait(3)

        # First matrix: model view
        matrix_group[2].to_corner(RIGHT + UP)
        matrix_group[5].next_to(matrix_group[2], DOWN)
        self.begin_ambient_camera_rotation(-0.05)
        self.move_camera(
            phi=55 * DEGREES,
            frame_center=ORIGIN,
            added_anims=[
                *self.swap_caption(
                    "The first matrix we're going to use is meant to realign the scene, such that the camera is located at the origin.",
                    t2c={"camera": "#FFFF00", "origin": "#FFFF00"}
                ),
                FadeIn(matrix_group[2], shift=LEFT),
                FadeIn(matrix_group[5], shift=LEFT),
            ]
        )
        self.wait(1.5)

        # Realign camera/scene
        to_rotate_group = Group(*object_group, *camera_group, *unit_cube_group)
        to_rotate_group.generate_target()
        to_rotate_group.target.shift(-CAMERA_POSITION).rotate_about_origin(-CAMERA_THETA, OUT).rotate_about_origin(-CAMERA_PHI, RIGHT)
        self.move_camera(
            frame_center = UP * 3,
            added_anims=[
                MoveToTarget(to_rotate_group),
            ],
            run_time = 2.5
        )
        self.wait(2)

        self.play(
            *self.swap_caption(
                "The camera should also face the negative Z-axis, such that X points right and Y points up, like in a normal graph.",
                t2c={"negative Z-axis": "#FFFF00"}
            ),
        )
        self.wait(3.5)

        self.play(
            *self.swap_caption(
                "The actual values in the Model View Matrix depend on the position and orientation of the camera.",
            ),
        )
        self.wait(3.5)

        self.play(
            *self.swap_caption(
                "Now that all coordinates are relative to the camera, we can move on to projection.",
                t2c={"projection": "#FFFF00"}
            ),
            FadeOut(matrix_group[2], shift=RIGHT),
            FadeOut(matrix_group[5], shift=RIGHT),
        )
        self.wait(3.5)

        # Second matrix: projection
        matrix_group[1].to_corner(RIGHT + UP)
        matrix_group[4].next_to(matrix_group[1], DOWN)
        self.play(
            *self.swap_caption(
                "The second matrix we'll be using is a little complicated, so let's analyze the variables first.",
            ),
            FadeIn(matrix_group[1], shift=LEFT),
            FadeIn(matrix_group[4], shift=LEFT),
        )
        self.wait(4)

        self.play(
            *self.swap_caption(
                "There are four variables: f, aspect, near and far.",
                t2c={"[22:23]": "#FFFF3F", "aspect": "#7FFF7F", "near": "#FFBF7F", "far": "#FF7FBF"}
            ),
        )
        self.wait(3.5)

        # Describe f
        self.play(
            *self.swap_caption(
                "f is the focal distance, which indicates how much the camera zooms in.",
                t2c={"[0:1]": "#FFFF3F"}
            ),
        )
        self.wait(3.5)

        # Adjust f
        to_stretch_group = Group(*camera_group[1:], *unit_cube_group)
        to_stretch_group.generate_target()
        to_stretch_group.target.stretch(0.5, 0, about_point=ORIGIN).stretch(0.5, 2, about_point=ORIGIN)
        self.play(
            MoveToTarget(to_stretch_group),
            *self.swap_caption(
                "If f gets larger, the camera's vision gets smaller, and it will seem as if the camera has zoomed in.",
                t2c={"[2:3]": "#FFFF3F"}
            ),
        )
        self.wait(3.5)

        # Describe aspect
        to_stretch_group.generate_target()
        to_stretch_group.target.stretch(2, 0, about_point=ORIGIN).stretch(2, 2, about_point=ORIGIN)
        self.play(
            MoveToTarget(to_stretch_group),
            *self.swap_caption(
                "aspect defines the aspect ratio of the image. This is needed when making non-square images.",
                t2c={"[0:6]": "#7FFF7F"}
            ),
        )
        self.wait(4)

        # Show aspect squish
        to_squish_group = Group(*camera_group[1:], *unit_cube_group, *object_group)
        self.play(
            *self.swap_caption(
                "This is because after projection, the scene is put inside a cube, so it should be horizontally \"squished\" to fit.",
                t2c={"cube": "#FFFF00"}
            ),
        )
        self.wait(1)
        self.play(
            to_squish_group.animate.stretch(1 / ASPECT, 0, about_point = ORIGIN),
            run_time = 0.8
        )
        self.wait(1)
        self.play(
            to_squish_group.animate.stretch(ASPECT, 0, about_point = ORIGIN),
            run_time = 0.8
        )
        self.wait(2)

        # Describe near and far
        self.play(
            *self.swap_caption(
                "Lastly, near and far are positive values which determine the distances of the near-plane and the far-plane from the camera.",
                t2c={"near": "#FFBF7F", "far": "#FF7FBF"}
            ),
        )
        self.wait(1)

        # Adjust near and far
        near_group = unit_cube_group[4:8]
        near_group.generate_target()
        near_group.target.scale(3, about_point=ORIGIN)
        far_group = unit_cube_group[8:]
        far_group.generate_target()
        far_group.target.scale(1.2, about_point=ORIGIN)
        self.play(
            MoveToTarget(near_group),
            MoveToTarget(far_group),
            run_time=0.5
        )
        self.wait(0.8)
        near_group.target.scale(0.5, about_point=ORIGIN)
        far_group.target.scale(0.4, about_point=ORIGIN)
        self.play(
            MoveToTarget(near_group),
            MoveToTarget(far_group),
            run_time=0.5
        )
        self.wait(0.8)
        near_group.target.scale(1 / (3 * 0.5), about_point=ORIGIN)
        far_group.target.scale(1 / (1.2 * 0.4), about_point=ORIGIN)
        self.play(
            MoveToTarget(near_group),
            MoveToTarget(far_group),
            run_time=0.5
        )
        self.wait(2)

        self.play(
            *self.swap_caption(
                "Everything between the near- and far-plane will be rendered, but everything in front of the near-plane or behind the far-plane will not.",
                t2c={"near": "#FFBF7F", "far": "#FF7FBF"}
            ),
        )
        self.wait(5)

        # Define projection functions
        projection_matrix = np.array([
            [F / ASPECT, 0, 0, 0],
            [0, F, 0, 0],
            [0, 0, (NEAR + FAR) / (NEAR - FAR), (2 * NEAR * FAR) / (NEAR - FAR)],
            [0, 0, -1, 0]
        ])
        projection_matrix_inverse = np.linalg.inv(projection_matrix)
        
        # Show frustrum
        frustrum = Cube(fill_color="#FFFF7F", stroke_width=0).set_opacity(0.25)
        frustrum.z_index = 1
        self.play(
            ApplyPointwiseFunction(
                lambda point: apply_transformation(projection_matrix_inverse, point),
                frustrum
            ),
            run_time=0
        )
        self.remove(frustrum)
        self.play(
            *self.swap_caption(
                "This means that only objects within this space are rendered to the image.",
            ),
            FadeIn(frustrum)
        )
        self.wait(3)

        self.play(
            *self.swap_caption(
                "This space is called a \"frustrum\", and its shape is influenced by f, aspect, near and far, as seen before.",
                t2c={"[54:55]": "#FFFF3F", "aspect": "#7FFF7F", "near": "#FFBF7F", "far": "#FF7FBF"}
            ),
        )
        self.wait(4)

        self.play(
            *self.swap_caption(
                "The idea of projection is to transform the frustrum to a cube from (-1, -1, -1) to (1, 1, 1).",
                t2c={"projection": "#FFFF00", "(-1, -1, -1)": "#FFFF00", "(1, 1, 1)": "#FFFF00"}
            ),
        )
        self.wait(4)

        self.play(
            FadeOut(frustrum),
            *self.swap_caption(
                "This is done using the Projection Matrix, which turns the scene into this:",
            ),
        )
        self.wait(1)

        # Apply projection to scene
        to_project_group = Group(*object_group, *unit_cube_group)
        self.move_camera(
            frame_center=ORIGIN,
            added_anims=[
                FadeOut(camera_group),
                ApplyPointwiseFunction(
                    lambda point: apply_transformation(projection_matrix, point),
                    to_project_group
                ),
            ],
            run_time = 2.5
        )
        self.wait(3)

        # Invert Z-axis
        self.stop_ambient_camera_rotation()
        self.move_camera(
            theta=-70 * DEGREES,
            phi=70 * DEGREES,
            added_anims=[
                *self.swap_caption(
                    "Side note: from here on out, we'll have the Z-axis pointing the opposite way, such that X points right, Y points up, and Z points away from the camera.",
                ),
            ]
        )
        self.wait(1)

        to_invert_group = Group(*axes_group[:1], *axes_group[5:], *object_group, *unit_cube_group)
        self.play(
            to_invert_group.animate.stretch(-1, 1, about_point=ORIGIN)
        )
        self.wait(3)

        to_squish_group = Group(*object_group, *unit_cube_group)
        self.move_camera(
            theta=-90 * DEGREES,
            phi=90 * DEGREES,
            frame_center=UP * 8,
            added_anims=[
                FadeOut(negative_z_label),
                FadeOut(positive_z_label),
                *self.swap_caption(
                    "This projection was the most important step, as we now have a 3D-looking scene in 2D.",
                ),
                FadeOut(matrix_group[1], shift=RIGHT),
                FadeOut(matrix_group[4], shift=RIGHT),
            ]
        )
        self.wait(4)

        # Show flattened projected cube
        self.play(
            to_squish_group.animate.stretch(0.01, 1, about_point=ORIGIN),
            *self.swap_caption(
                "If the cube is flattened, you can see how this scene still seems to have perspective, despite being flat.",
            ),
        )
        self.wait(4)

        self.move_camera(
            frame_center=ORIGIN,
            added_anims=[
                to_squish_group.animate.stretch(100, 1, about_point=ORIGIN),
                *self.swap_caption(
                    "However, we don't flatten the cube, since we should still use the Z-coordinate later to determine which objects are in front.",
                ),
            ]
        )
        self.wait(5)

        self.play(
            *self.swap_caption(
                "We have now managed to create perspective in 2D, which is what we want, but there is still a small problem.",
            ),
        )
        self.wait(4)

        self.play(
            *self.swap_caption(
                "Our cube here is small, and screens don't count pixels from -1 to 1.",
            ),
        )
        self.wait(3)

        # Third matrix: viewport
        matrix_group[0].to_corner(RIGHT + UP)
        matrix_group[3].next_to(matrix_group[0], DOWN)
        self.play(
            FadeIn(matrix_group[0], shift=LEFT),
            FadeIn(matrix_group[3], shift=LEFT),
            *self.swap_caption(
                "To solve this, we use the Viewport Matrix, which just scales and translates the scene by a certain amount.",
                pos=DOWN * 3.1
            ),
        )
        self.wait(1)

        # Apply viewport matrix
        scale = 2 / 1080
        height = 5
        width = height * ASPECT
        new_center = np.array([-width / 2, 0, -height / 2])
        to_scale_group = Group(*object_group, *unit_cube_group)
        all_group = Group(*axes_group, to_scale_group)
        self.play(
            all_group.animate.shift(new_center)
        )
        self.play(
            to_scale_group.animate.shift((1, 0, 1))
        )
        self.play(
            all_group.animate.scale(scale, about_point=new_center)
        )
        to_scale_group.generate_target()
        to_scale_group.target.stretch(0.5 * width / scale, dim=0, about_point=new_center)
        to_scale_group.target.stretch(50, dim=1, about_point=new_center)
        to_scale_group.target.stretch(0.5 * height / scale, dim=2, about_point=new_center)
        self.play(
            MoveToTarget(to_scale_group)
        )

        self.play(
            *self.swap_caption(
                "Now each position correponds to a pixel between (0, 0) and, e.g., (1919, 1079), which the computer understands.",
                pos=DOWN * 3.1
            ),
        )
        self.wait(4)

        # Voilá!
        self.move_camera(
            frame_center=[0, -3, 0],
            added_anims=[
                *self.swap_caption(
                    "And voilá! A camera projection, made with a 3D scene and just three matrix transformations.",
                    pos=DOWN * 3.1
                ),
                FadeOut(matrix_group[0], shift=RIGHT),
                FadeOut(matrix_group[3], shift=RIGHT),
            ]
        )
        self.wait(2.5)

HIGH_QUALITY = True
START_AT = 0
END_AT = 1000

if __name__ == "__main__":
    render_video(os.path.realpath(__file__), HIGH_QUALITY, START_AT, END_AT)