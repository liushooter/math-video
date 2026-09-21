# 正弦与余弦曲线

基于相邻目录 `../manim` 的 3Blue1Brown Manim，绘制 `y = sin(x)` 和
`y = cos(x)`。横轴范围为 −2π 到 2π，蓝色为正弦，橙色为余弦。
动画约 11 秒，1080p、30 fps；文字使用 Heiti SC，不需要 LaTeX。

## 运行

```sh
uv venv .venv --python 3.12
uv pip install --python .venv/bin/python -r ../manim/requirements.txt
sh render.sh
sh render.sh -s
```

分别生成 `output/trig_curves.mp4` 和 `output/trig_curves.png`。
可通过 `MANIM_PATH` 指定另一个本地 Manim 源码目录。
视频、图片、依赖和缓存不纳入 Git。

## 背景音乐

渲染完成后运行 `.venv/bin/python add_bgm.py`（需要系统已安装 FFmpeg），
生成轻柔电子琴琶音配乐版 `output/trig_curves_bgm.mp4`，
以及独立音轨 `output/trig_bgm.wav`。配乐由代码合成，带淡入淡出，
视频画面直接复制，原视频保留。
