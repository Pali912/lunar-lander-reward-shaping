"""Turn recorded videos into small GIFs for the README.

Run with the venv active:
    python make_gifs.py
Reads clips from videos/, writes GIFs to assets/.
"""
import os

from moviepy import VideoFileClip

# Each GIF tries the file names in order (the first baseline clips were
# recorded before play.py started naming videos after the model).
CLIPS = {
    "baseline": [
        "videos/baseline-episode-0.mp4",
        "videos/ppo_baseline-episode-0.mp4",
    ],
    "hover_hack": ["videos/ppo_hover_hack-episode-0.mp4"],
    "improvement_fix": ["videos/ppo_improvement_fix-episode-0.mp4"],
}
MAX_SECONDS = 12
WIDTH = 400
FPS = 15

os.makedirs("assets", exist_ok=True)

for name, candidates in CLIPS.items():
    path = next((p for p in candidates if os.path.exists(p)), None)
    if path is None:
        print(f"{name}: no video found, looked for {candidates}")
        continue
    clip = VideoFileClip(path)
    clip = clip.subclipped(0, min(clip.duration, MAX_SECONDS)).resized(width=WIDTH)
    out = f"assets/{name}.gif"
    clip.write_gif(out, fps=FPS)
    clip.close()
    print(f"{name}: wrote {out} ({os.path.getsize(out) / 1e6:.1f} MB) from {path}")
