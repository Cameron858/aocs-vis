from manim import *


class CoordinateFrames(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        axes = ThreeDAxes()
        self.play(Create(axes))
        self.wait()

        axis_color_sweeps = [
            (
                axis,
                color,
                Line(axis.get_start(), axis.get_end(), color=color, stroke_width=4),
            )
            for axis, color in (
                (axes.x_axis, RED),
                (axes.y_axis, GREEN),
                (axes.z_axis, BLUE),
            )
        ]
        self.play(
            *(Create(sweep) for _, _, sweep in axis_color_sweeps),
            run_time=1,
        )
        self.play(
            *(axis.animate.set_color(color) for axis, color, _ in axis_color_sweeps),
            *(FadeOut(sweep) for _, _, sweep in axis_color_sweeps),
            run_time=0.2,
        )

        x_label = Text("X", color=RED).move_to(axes.x_axis.get_end() + 0.3 * RIGHT)
        y_label = Text("Y", color=GREEN).move_to(axes.y_axis.get_end() + 0.3 * UP)
        z_label = (
            Text("Z", color=BLUE)
            .rotate(90 * DEGREES, axis=RIGHT)
            .move_to(axes.z_axis.get_end() + 0.3 * OUT)
        )
        self.play(FadeIn(x_label, y_label, z_label))
        self.wait()

        RATE = 1.5
        self.begin_ambient_camera_rotation(RATE)
        self.wait(2 * PI / RATE)
        self.stop_ambient_camera_rotation()

        self.wait()

        body_origin = 2 * RIGHT + 2 * UP + 2 * OUT
        body_cube = Cube(side_length=0.5).move_to(body_origin)
        self.play(FadeIn(body_cube, scale=0.1))

        for direction, color in (
            (RIGHT, RED),
            (UP, GREEN),
            (OUT, BLUE),
        ):
            body_vector = Arrow3D(
                start=body_origin,
                end=body_origin + direction,
                color=color,
            )
            self.play(Create(body_vector))

        self.wait(2)
