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
    """在同一坐标系中绘制两个周期的正弦、余弦，并展示相位关系。"""

    # 关闭合并绘制与绘制指令复用，使用逐对象绘制的渲染配置。
    default_camera_config = {"draw_together": False, "bundle_draws": False}

    def construct(self):
        """Manim 场景入口：创建图形，并按时间顺序编排动画。"""
        # 两种亮色区分函数；灰色用于坐标轴和辅助说明。
        blue, orange, muted = "#63D5F4", "#FFB66E", "#94A3B8"

        def label(text, size=25, color="#E8EEF6"):
            """统一文字样式，使用本机中文字体，无需依赖 LaTeX。"""
            return (
                Text(text, font="Heiti SC", font_size=size)
                .set_color(color)
                .set_stroke(width=0)
            )

        # 布局距离使用 Manim 场景单位，而非像素；buff 表示对象间留白。
        title = label("正弦曲线与余弦曲线", 44).to_edge(UP, buff=0.55)
        legend = (
            VGroup(
                label("正弦  y = sin(x)", 28, blue),
                label("余弦  y = cos(x)", 28, orange),
            )
            .arrange(RIGHT, buff=1.2)
            .move_to(UP * 2.6)
        )

        # range 的三个值依次为起点、终点、刻度间隔。
        # 横轴覆盖两个周期；纵轴在函数值域 [-1, 1] 上下各留出 0.5。
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
        # c2p 将数学坐标转换为场景坐标，确保网格与缩放、平移后的轴对齐。
        grid = VGroup()
        # arange 不包含右端点，略微扩大终点以纳入 2π 处的网格线。
        for x in np.arange(-2 * np.pi, 2.01 * np.pi, np.pi / 2):
            # x=0 已有纵轴，避免重复绘制；容差用于处理浮点误差。
            if abs(x) > 1e-6:
                grid.add(Line(axes.c2p(x, -1.35), axes.c2p(x, 1.35)))
        for y in (-1, -0.5, 0.5, 1):
            grid.add(Line(axes.c2p(-2 * np.pi, y), axes.c2p(2 * np.pi, y)))
        grid.set_stroke("#27364A", width=1)

        # 手动添加 π 形式的横轴标签，比小数弧度更容易辨认特殊角度。
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

        # get_graph 按坐标轴范围生成曲线；NumPy 三角函数的输入单位是弧度。
        sine = axes.get_graph(np.sin, color=blue, stroke_width=4)
        cosine = axes.get_graph(np.cos, color=orange, stroke_width=4)
        dots = VGroup(Dot(color=blue, radius=0.065), Dot(color=orange, radius=0.065))

        def move_dots(group, alpha):
            """将动画进度 alpha（0～1）映射为横坐标，并更新两个指示点。"""
            x = -2 * np.pi + 4 * np.pi * alpha
            group[0].move_to(axes.c2p(x, np.sin(x)))
            group[1].move_to(axes.c2p(x, np.cos(x)))

        # 先把指示点放在曲线左端，避免入场时出现在默认原点。
        move_dots(dots, 0)
        footer = label("振幅 1   ·   周期 2π   ·   x 为弧度", 25, muted).to_edge(
            DOWN, buff=0.75
        )
        relation = label("cos(x) = sin(x + π/2)", 25).next_to(footer, UP, buff=0.22)
        # 同一次 play 中的动画并行执行，不同 play 调用按顺序执行。
        self.play(FadeIn(title), FadeIn(legend), run_time=0.8)
        self.play(FadeIn(grid), FadeIn(axes), FadeIn(ticks), run_time=0.8)
        self.add(dots)
        # 六秒内同时画出两条曲线，并以匀速横向移动指示点。
        # 使用动画回调更新位置，只在这段动画执行期间计算。
        self.play(
            ShowCreation(sine),
            ShowCreation(cosine),
            UpdateFromAlphaFunc(dots, move_dots),
            run_time=6,
            rate_func=linear,
        )
        # 移除指示点后展示函数性质，并停留供观众阅读；总时长为 11 秒。
        self.play(FadeOut(dots), FadeIn(footer), FadeIn(relation), run_time=0.8)
        self.wait(2.6)
