#!/bin/sh
# 遇到命令失败或未定义变量时退出，防止带着错误继续渲染。
set -eu
# 从脚本所在目录运行，使相对路径不受调用位置影响。
cd "$(dirname "$0")"
# 优先加载本地 Manim 源码；可用 MANIM_PATH 覆盖默认的相邻目录。
export PYTHONPATH="${MANIM_PATH:-../manim}${PYTHONPATH:+:$PYTHONPATH}"
# 为遵循 XDG 约定的工具和 Matplotlib 指定项目内缓存目录。
# macOS 上 Manim 自身的缓存仍由其默认配置决定。
export XDG_CACHE_HOME="$PWD/.cache"
export MPLCONFIGDIR="$PWD/.cache/matplotlib"
# 默认导出 1080p、30 fps 视频；透传参数，例如 -s 可改为导出最终帧。
.venv/bin/python -m manimlib trig_curves.py TrigCurves -w --hd \
  --fps 30 -c '#101827' --video_dir output --file_name trig_curves "$@"
