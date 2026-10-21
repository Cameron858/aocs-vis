from manim import *


class CoordinateFrames(ThreeDScene):
    def rotate_camera(self):
        RATE = 1.5
        self.begin_ambient_camera_rotation(RATE)
        self.wait(TAU / RATE)
        self.stop_ambient_camera_rotation()

    def rotate_about_inertial_axis(
        self,
        mobject,
        axis,
        angle=TAU,
        about_point=ORIGIN,
        axis_length=5,
        run_time=4,
        pause=0.5,
    ):
        axis = normalize(axis)
        axis_line = DashedLine(about_point, about_point + axis_length * axis)
        self.play(Create(axis_line))
        self.play(
            Rotate(mobject, angle=angle, axis=axis, about_point=about_point),
            run_time=run_time,
        )
        self.wait(pause)
        self.play(FadeOut(axis_line))

    def rotate_about_body_axis(
        self,
        mobject,
        axis,
        body_axes,
        angle=TAU,
        axis_length=5,
        run_time=4,
        pause=0.5,
    ):
        axis = normalize(
            sum(
                (
                    component * normalize(body_axis.get_end() - body_axis.get_start())
                    for component, body_axis in zip(axis, body_axes, strict=True)
                ),
                start=ORIGIN,
            )
        )
        about_point = body_axes[0].get_start()
        axis_line = DashedLine(about_point, about_point + axis_length * axis)
        self.play(Create(axis_line))
        self.play(
            Rotate(mobject, angle=angle, axis=axis, about_point=about_point),
            run_time=run_time,
        )
        self.wait(pause)
        self.play(FadeOut(axis_line))

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

        x_label = (
            MathTex(r"\epsilon_1")
            .set_color(RED)
            .move_to(axes.x_axis.get_end() + 0.3 * RIGHT)
        )
        y_label = MathTex(r"\epsilon_2", color=GREEN).move_to(
            axes.y_axis.get_end() + 0.3 * UP
        )
        z_label = (
            MathTex(r"\epsilon_3", color=BLUE)
            .rotate(90 * DEGREES, axis=RIGHT)
            .move_to(axes.z_axis.get_end() + 0.3 * OUT)
        )
        self.play(FadeIn(x_label, y_label, z_label))
        self.wait()

        body_origin = 2 * RIGHT + 2 * UP + 2 * OUT
        body_cube = Cube(side_length=0.5).move_to(body_origin)
        self.play(FadeIn(body_cube, scale=0.1))

        body_vectors = [
            Arrow3D(
                start=body_origin,
                end=body_origin + direction,
                color=color,
            )
            for direction, color in (
                (RIGHT, RED),
                (UP, GREEN),
                (OUT, BLUE),
            )
        ]
        self.play(
            *(
                GrowFromPoint(body_vector, point=body_origin)
                for body_vector in body_vectors
            )
        )

        body_frame = VGroup(body_cube, *body_vectors)
        self.move_camera(
            phi=75 * DEGREES,
            theta=0 * DEGREES,
            frame_center=body_origin,
            run_time=1.5,
        )
        self.rotate_about_body_axis(
            body_frame,
            axis=[1, -1, 1],
            body_axes=body_vectors,
            angle=TAU,
        )

        self.move_camera(
            phi=75 * DEGREES,
            theta=45 * DEGREES,
            frame_center=body_origin,
            run_time=1.5,
        )
        self.rotate_about_body_axis(
            body_frame,
            axis=[0, 1, 1],
            body_axes=body_vectors,
            angle=TAU,
        )

        # final wait
        self.wait(2)
