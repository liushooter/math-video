"""为三角函数动画合成轻柔的背景音乐，并无损复制视频画面。"""

import json
from pathlib import Path
import subprocess
import wave

import numpy as np


def main():
    root = Path(__file__).resolve().parent
    source = root / "output/trig_curves.mp4"
    music = source.with_name("trig_bgm.wav")
    target = source.with_name("trig_curves_bgm.mp4")
    info = json.loads(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_format", "-of", "json", str(source)]
        )
    )
    duration = float(info["format"]["duration"])
    rate = 48000
    audio = np.zeros((round(duration * rate), 2))

    def note(midi, start, length, gain, pan=0.0, pad=False):
        offset = round(start * rate)
        count = min(round(length * rate), len(audio) - offset)
        if count <= 0:
            return
        t = np.arange(count) / rate
        frequency = 440 * 2 ** ((midi - 69) / 12)
        tone = (
            np.sin(2 * np.pi * frequency * t)
            + 0.22 * np.sin(2 * np.pi * frequency * 2 * t)
            + 0.06 * np.sin(2 * np.pi * frequency * 3 * t)
        )
        attack = 0.35 if pad else 0.018
        envelope = (1 - np.exp(-t / attack)) * np.exp(-t / (2 if pad else 0.65))
        envelope *= np.minimum(1, np.maximum(0, (length - t) / 0.4))
        tone *= envelope * gain
        audio[offset : offset + count, 0] += tone * np.sqrt((1 - pan) / 2)
        audio[offset : offset + count, 1] += tone * np.sqrt((1 + pan) / 2)

    # Cmaj7 → Am7 → Fmaj7 → Cmaj9，最后一个和弦留出消散时间。
    chords = [(48, 55, 59, 64), (45, 52, 55, 60), (41, 48, 52, 57), (48, 55, 62, 64)]
    beat = duration / 16
    for bar, chord in enumerate(chords):
        start = bar * 4 * beat
        for pitch in chord:
            note(pitch, start, 4 * beat + 0.6, 0.032, pad=True)
        pattern = (0, 2, 1, 3, 2, 1, 3, 2) if bar < 3 else (0, 1, 2, 3)
        for step, index in enumerate(pattern):
            when = start + step * beat / 2
            pan = -0.22 if step % 2 == 0 else 0.22
            note(chord[index] + 12, when, 1.7, 0.10, pan)
            note(chord[index] + 12, when + 0.19, 1.5, 0.018, -pan)

    t = np.arange(len(audio)) / rate
    fade = np.minimum(1, t / 0.35) * np.clip((duration - t) / 1.3, 0, 1)
    audio *= fade[:, None]
    audio *= 0.24 / max(np.max(np.abs(audio)), 1e-9)
    with wave.open(str(music), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(rate)
        wav.writeframes((audio * 32767).astype("<i2").tobytes())
    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(source),
            "-i",
            str(music),
            "-map",
            "0:v:0",
            "-map",
            "1:a:0",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-t",
            str(duration),
            "-movflags",
            "+faststart",
            str(target),
        ],
        check=True,
    )
    print(target)


if __name__ == "__main__":
    main()
