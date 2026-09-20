#!/bin/sh
set -eu
cd "$(dirname "$0")"
export PYTHONPATH="${MANIM_PATH:-../manim}${PYTHONPATH:+:$PYTHONPATH}"
export XDG_CACHE_HOME="$PWD/.cache"
export MPLCONFIGDIR="$PWD/.cache/matplotlib"
.venv/bin/python -m manimlib trig_curves.py TrigCurves -w --hd \
  --fps 30 -c '#101827' --video_dir output --file_name trig_curves "$@"
