from manim import *


class CoordinateFrames(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        x_label = Text("X").move_to(axes.x_axis.get_end() + 0.3 * RIGHT)
        y_label = Text("Y").move_to(axes.y_axis.get_end() + 0.3 * UP)
        z_label = (
            Text("Z")
            .rotate(90 * DEGREES, axis=RIGHT)
            .move_to(axes.z_axis.get_end() + 0.3 * OUT)
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

        self.play(Create(axes))
        self.wait(1)
        self.play(FadeIn(x_label, y_label, z_label))
        self.wait(1)

        for axis, label, color in (
            (axes.x_axis, x_label, RED),
            (axes.y_axis, y_label, GREEN),
            (axes.z_axis, z_label, BLUE),
        ):
            color_sweep = Line(
                axis.get_start(), axis.get_end(), color=color, stroke_width=4
            )
            self.play(Create(color_sweep), run_time=1)
            self.play(
                axis.animate.set_color(color),
                label.animate.set_color(color),
                FadeOut(color_sweep),
                run_time=0.2,
            )

        RATE = 2
        self.begin_ambient_camera_rotation(RATE)
        self.wait(2 * PI / RATE)
        self.stop_ambient_camera_rotation()

        self.wait(1)
