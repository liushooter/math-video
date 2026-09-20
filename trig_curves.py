"""使用相邻目录的 3Blue1Brown Manim 绘制正弦与余弦曲线。"""

import numpy as np
from manimlib import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Axes,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    Scene,
    ShowCreation,
    Text,
    UpdateFromAlphaFunc,
    VGroup,
    linear,
)


class TrigCurves(Scene):
    default_camera_config = {"draw_together": False, "bundle_draws": False}

    def construct(self):
        blue, orange, muted = "#63D5F4", "#FFB66E", "#94A3B8"

        def label(text, size=25, color="#E8EEF6"):
            return (
                Text(text, font="Heiti SC", font_size=size)
                .set_color(color)
                .set_stroke(width=0)
            )

        title = label("正弦曲线与余弦曲线", 44).to_edge(UP, buff=0.55)
        legend = (
            VGroup(
                label("正弦  y = sin(x)", 28, blue),
                label("余弦  y = cos(x)", 28, orange),
            )
            .arrange(RIGHT, buff=1.2)
            .move_to(UP * 2.6)
        )

        axes = Axes(
            x_range=(-2 * np.pi, 2 * np.pi, np.pi / 2),
            y_range=(-1.5, 1.5, 0.5),
            width=11.6,
            height=4.1,
            axis_config={
                "stroke_color": muted,
                "stroke_width": 2,
                "include_tip": False,
            },
        ).shift(DOWN * 0.35)
        grid = VGroup()
        for x in np.arange(-2 * np.pi, 2.01 * np.pi, np.pi / 2):
            if abs(x) > 1e-6:
                grid.add(Line(axes.c2p(x, -1.35), axes.c2p(x, 1.35)))
        for y in (-1, -0.5, 0.5, 1):
            grid.add(Line(axes.c2p(-2 * np.pi, y), axes.c2p(2 * np.pi, y)))
        grid.set_stroke("#27364A", width=1)

        ticks = VGroup()
        for x, text in zip(
            np.arange(-2 * np.pi, 2.01 * np.pi, np.pi / 2),
            ("−2π", "−3π/2", "−π", "−π/2", "0", "π/2", "π", "3π/2", "2π"),
        ):
            ticks.add(label(text, 20, muted).next_to(axes.c2p(x, 0), DOWN, buff=0.16))
        for y in (-1, 1):
            ticks.add(label(str(y), 20, muted).next_to(axes.c2p(0, y), LEFT, buff=0.16))
        ticks.add(label("x", 23, muted).next_to(axes.c2p(2 * np.pi, 0), RIGHT))
        ticks.add(label("y", 23, muted).next_to(axes.c2p(0, 1.5), UP, buff=0.1))

        sine = axes.get_graph(np.sin, color=blue, stroke_width=4)
        cosine = axes.get_graph(np.cos, color=orange, stroke_width=4)
        dots = VGroup(Dot(color=blue, radius=0.065), Dot(color=orange, radius=0.065))

        def move_dots(group, alpha):
            x = -2 * np.pi + 4 * np.pi * alpha
            group[0].move_to(axes.c2p(x, np.sin(x)))
            group[1].move_to(axes.c2p(x, np.cos(x)))

        move_dots(dots, 0)
        footer = label("振幅 1   ·   周期 2π   ·   x 为弧度", 25, muted).to_edge(
            DOWN, buff=0.75
        )
        relation = label("cos(x) = sin(x + π/2)", 25).next_to(footer, UP, buff=0.22)
        self.play(FadeIn(title), FadeIn(legend), run_time=0.8)
        self.play(FadeIn(grid), FadeIn(axes), FadeIn(ticks), run_time=0.8)
        self.add(dots)
        self.play(
            ShowCreation(sine),
            ShowCreation(cosine),
            UpdateFromAlphaFunc(dots, move_dots),
            run_time=6,
            rate_func=linear,
        )
        self.play(FadeOut(dots), FadeIn(footer), FadeIn(relation), run_time=0.8)
        self.wait(2.6)
