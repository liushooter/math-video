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
