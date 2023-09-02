from imports import *
from manim import *
import numpy as np

class MainScene(CGScene):
    def get_title(self):
        return "Texture Coordinates"

    def animate(self):
        IMAGE_PATTERN = [
            ".............YYY",
            "......RRRRR..YYY",
            ".....RRRRRRRRRYY",
            ".....GGGYYGY.GGG",
            "....GYGYYYGYYGGG",
            "....GYGGYYYGYYYG",
            "....GGYYYYGGGGG.",
            "......YYYYYYYG..",
            "..GGGGGRGGGRG...",
            ".GGGGGGGRGGGR..G",
            "YYGGGGGGRRRRR..G",
            "YYY.RRGRRYRRYRGG",
            ".Y.GRRRRRRRRRRGG",
            "..GGGRRRRRRRRRGG",
            ".GGGRRRRRRR.....",
            ".G..RRRR........",
        ]
        COLOR_MAP = {
            ".": "#9F9FFF",
            "R": "#FF0000",
            "Y": "#FFBF00",
            "G": "#9F7F00",
        }
        RED = "#FF1F1F"
        GREEN = "#00DF00"
        BLUE = "#007FFF"
        COLORS = [RED, GREEN, BLUE]
        OFFSET = 3.5

        def normalize(v):
            norm = np.linalg.norm(v)
            if norm == 0:
                return v
            return v / norm

        source_texture = Group()
        for iy in range(len(IMAGE_PATTERN)):
            for ix in range(len(IMAGE_PATTERN[0])):
                color = COLOR_MAP[IMAGE_PATTERN[iy][ix]]
                square = Polygon(ORIGIN, UP, UP + RIGHT, RIGHT).set_stroke(color, opacity=1, width=0.6).set_fill(color, opacity=1)
                square.move_to((ix, -iy, 0))
                square.set_z_index(15)
                source_texture.add(square)

        source_texture.scale(0.25).move_to((-OFFSET, 0, 0))
        self.play(
            FadeIn(source_texture)
        )

        destination_texture = Group(*[j.copy() for j in source_texture])
        destination_texture.shift(2 * OFFSET * RIGHT).set_z_index(5)
        for square in destination_texture:
            square.save_state()

        # Create triangles
        triangles = {}
        for ty in "tp":
            points = []
            for i in range(3):
                point = Circle(0.08)
                point.set_stroke("#FFFFFF", width=5).set_fill(COLORS[i], opacity=1)
                point.set_z_index(25)
                points.append(point)
            for i in range(3):
                points[i].neighbors = [points[i - 1], points[i - 2]]
            points[0].shift((-1.5, -1, 0))
            points[1].shift((1.5, -1, 0))
            points[2].shift((0, 1, 0))

            lines = []
            for i in range(3):
                line = Line().set_stroke("#FFFFFF", width=5)
                line.set_z_index(20)
                line.ends = [points[i - 2], points[i - 1]]
                line_updater = lambda m: m.put_start_and_end_on(m.ends[0].get_center(), m.ends[1].get_center())
                line_updater(line)
                line.add_updater(line_updater)
                lines.append(line)

            def align_label(obj):
                a = obj.point.get_center()
                b = obj.point.neighbors[0].get_center()
                c = obj.point.neighbors[1].get_center()

                p = normalize(a - b)
                q = normalize(a - c)
                d = normalize(p + q)
                obj.move_to(a + d * 0.3)

            labels = []
            for i in range(3):
                label = Tex(f"${ty}_{i}$")
                label.set_color("#FFFFFF").set_background_stroke(color=COLORS[i], width=3)
                label.scale(0.6).set_z_index(30)
                label.point = points[i]
                label_updater = lambda m: align_label(m)
                label_updater(label)
                label.add_updater(label_updater)
                labels.append(label)

            triangles[ty] = (points, lines, labels)

        tc_points, tc_lines, tc_labels = triangles["t"]
        pc_points, pc_lines, pc_labels = triangles["p"]

        for obj in [*tc_points, *tc_lines, *tc_labels]:
            obj.shift((-OFFSET, 0, 0))
        for obj in [*pc_points, *pc_lines, *pc_labels]:
            obj.shift((OFFSET, 0, 0))

        self.play(
            *[FadeIn(j, scale=5) for j in tc_points],
            run_time=0.5
        )
        self.play(
            *[Create(j) for j in tc_lines],
            *[Write(j) for j in tc_labels],
            run_time=0.8
        )
        self.wait(1)

        self.play(
            *[FadeIn(j, scale=5) for j in pc_points],
            run_time=0.5
        )
        self.play(
            *[Create(j) for j in pc_lines],
            *[Write(j) for j in pc_labels],
            run_time=0.8
        )

        def keep_cover_in_place(cover):
            a = cover.point.get_center()
            b = cover.point.neighbors[0].get_center()
            c = cover.point.neighbors[1].get_center()

            mid = (b + c) / 2
            diff = c - b
            angle = np.angle(diff[0] + 1j * diff[1])
            p = b - c
            q = b - a
            q = np.array([-q[1], q[0], 0])
            if np.dot(p, q) < 0:
                angle += np.pi

            cover.restore()
            cover.move_to(mid + 25 * UP).rotate(angle, about_point=mid)

        covers = []
        for i in range(3):
            cover = Square(50)
            cover.set_stroke(opacity=0).set_fill(BACKGROUND_COLOR, opacity=1)
            cover.set_z_index(10)
            cover.point = pc_points[i]
            cover.save_state()

            keep_cover_in_place(cover)
            cover.add_updater(keep_cover_in_place)
            covers.append(cover)

        self.add(*covers)
        self.play(
            FadeIn(destination_texture),
            run_time=0.6
        )
        self.wait(2)

        def warp_points(points, matrix):
            for i in range(points.shape[0]):
                points[i] = matrix @ points[i]
            return points
        def warp_square(obj, matrix):
            obj.restore()
            obj.shift(2 * OFFSET * LEFT - tc_points[0].get_center())
            obj.apply_points_function_about_point(lambda points: warp_points(points, matrix), about_point=ORIGIN)
            obj.shift(pc_points[0].get_center())
        def warp_texture(obj):
            to_correct = 0
            tc_matrix = None
            a, b, c = [j.get_center() for j in tc_points]
            while True:
                tc_matrix = np.array([b - a, c - a, [0, 0, 1]]).T
                if to_correct == 6:
                    tc_matrix = np.identity(3)
                if abs(np.linalg.det(tc_matrix)) > 1e-6:
                    break
                [a, b, c][to_correct % 3][to_correct // 3] += 0.01
                to_correct += 1
            a, b, c = [j.get_center() for j in pc_points]
            pc_matrix = np.array([b - a, c - a, [0, 0, 1]]).T
            matrix = pc_matrix @ np.linalg.inv(tc_matrix)

            for square in obj:
                warp_square(square, matrix)

        destination_texture.add_updater(warp_texture)

        self.play(
            pc_points[0].animate.shift((0, -1, 0)),
            run_time=1.5
        )
        self.wait(1)

        self.play(
            pc_points[1].animate.shift((1, 0, 0)),
            pc_points[2].animate.shift((-1, -1, 0)),
            run_time=1.5
        )
        self.wait(1)

        self.play(
            pc_points[0].animate.shift((0, 1, 0)),
            pc_points[1].animate.shift((-1, 0, 0)),
            pc_points[2].animate.shift((1, 1, 0)),
            run_time=1.5
        )
        self.wait(1)

        self.play(
            tc_points[0].animate.shift((1, 0, 0)),
            tc_points[1].animate.shift((1, 0, 0)),
            tc_points[2].animate.shift((1, 0, 0)),
            run_time=1.5
        )
        self.wait(1)

        self.play(
            tc_points[0].animate.shift((-1, 1, 0)),
            tc_points[1].animate.shift((-1, 1, 0)),
            tc_points[2].animate.shift((-1, 1, 0)),
            run_time=1.5
        )
        self.wait(1)

        tc_points_group = Group(*tc_points)
        self.play(
            tc_points_group.animate.scale(0.5),
            run_time=1.5
        )
        self.wait(1)

        self.play(
            tc_points_group.animate.rotate(-np.pi / 2),
            run_time=1.5
        )
        self.wait(1)

        self.play(
            tc_points[1].animate.shift((-1.5, 0, 0)),
            run_time=1.5
        )
        self.wait(1)

        self.play(
            Rotate(tc_points_group, np.pi, about_point=source_texture.get_center()),
            run_time=1.5
        )
        self.wait(1)

HIGH_QUALITY = False
START_AT = 0
END_AT = 1000

if __name__ == "__main__":
    render_video(os.path.realpath(__file__), HIGH_QUALITY, START_AT, END_AT)