"""Build one labeled side-by-side video from the three recorded clips.

Run with the venv active, after recording the clips with play.py:
    python make_showcase.py
Reads clips from videos/, writes assets/showcase.mp4 and assets/showcase.gif.
"""
import os

import numpy as np
from moviepy import CompositeVideoClip, ImageClip, VideoFileClip, concatenate_videoclips
from PIL import Image, ImageDraw, ImageFont

# (title, subtitle, result line, candidate file names, accent color)
PANELS = [
    (
        "Normal landing",
        "Built-in reward only",
        "20-attempt average 250, lands in about 390 frames",
        ["videos/baseline-episode-0.mp4", "videos/ppo_baseline-episode-0.mp4"],
        (110, 200, 130),
    ),
    (
        "Reward hacked",
        "+1 per frame while upright and slow",
        "20-attempt average -26, hovers for all 1000 frames",
        ["videos/ppo_hover_hack-episode-0.mp4"],
        (235, 90, 90),
    ),
    (
        "The fix",
        "Pay for improvement, plus a small fee per frame",
        "20-attempt average 238, lands in about 430 frames",
        ["videos/ppo_improvement_fix-episode-0.mp4"],
        (110, 170, 240),
    ),
]

MAX_SECONDS = 14      # trim long clips (the hover clip is 20 seconds)
PANEL_W, PANEL_H = 540, 360
GAP = 12
HEADER, FOOTER = 96, 76
W = 3 * PANEL_W + 4 * GAP          # 1668
H = HEADER + PANEL_H + FOOTER      # 532
OUT_FPS = 30
GIF_WIDTH, GIF_FPS = 900, 12
BACKGROUND = (20, 22, 28)
WHITE, GREY = (240, 240, 240), (165, 170, 180)


def load_font(size, bold=False):
    names = (
        ["C:/Windows/Fonts/segoeuib.ttf", "C:/Windows/Fonts/arialbd.ttf", "DejaVuSans-Bold.ttf"]
        if bold
        else ["C:/Windows/Fonts/segoeui.ttf", "C:/Windows/Fonts/arial.ttf", "DejaVuSans.ttf"]
    )
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def fit_text(draw, text, font, max_width):
    """Shorten text with ... if it is wider than max_width."""
    if draw.textlength(text, font=font) <= max_width:
        return text
    while text and draw.textlength(text + "...", font=font) > max_width:
        text = text[:-1]
    return text + "..."


def find_clip(candidates):
    return next((p for p in candidates if os.path.exists(p)), None)


def background():
    img = Image.new("RGB", (W, H), BACKGROUND)
    draw = ImageDraw.Draw(img)
    title_font, sub_font, foot_font = load_font(30, True), load_font(19), load_font(19)
    for i, (title, subtitle, result, _, accent) in enumerate(PANELS):
        x = GAP + i * (PANEL_W + GAP)
        draw.rectangle([x, 16, x + 6, 16 + 58], fill=accent)  # colored tab
        draw.text((x + 18, 12), fit_text(draw, title, title_font, PANEL_W - 20), font=title_font, fill=WHITE)
        draw.text((x + 18, 54), fit_text(draw, subtitle, sub_font, PANEL_W - 20), font=sub_font, fill=GREY)
        draw.rectangle([x - 2, HEADER - 2, x + PANEL_W + 1, HEADER + PANEL_H + 1], outline=accent, width=2)
        draw.text(
            (x, HEADER + PANEL_H + 18),
            fit_text(draw, result, foot_font, PANEL_W),
            font=foot_font,
            fill=WHITE,
        )
    return np.array(img)


def panel_clip(path, total):
    clip = VideoFileClip(path)
    clip = clip.subclipped(0, min(clip.duration, total)).resized((PANEL_W, PANEL_H))
    if clip.duration < total - 0.05:
        # Hold the last frame so a finished attempt stays on screen
        last = clip.get_frame(max(clip.duration - 0.05, 0))
        clip = concatenate_videoclips([clip, ImageClip(last).with_duration(total - clip.duration)])
    return clip


paths = [find_clip(p[3]) for p in PANELS]
missing = [p[3][0] for p, found in zip(PANELS, paths) if found is None]
if missing:
    raise SystemExit(f"Missing clips: {missing}. Record them with play.py record first.")

durations = []
for path in paths:
    c = VideoFileClip(path)
    durations.append(c.duration)
    c.close()
total = min(max(durations), MAX_SECONDS)

layers = [ImageClip(background()).with_duration(total)]
for i, path in enumerate(paths):
    x = GAP + i * (PANEL_W + GAP)
    layers.append(panel_clip(path, total).with_position((x, HEADER)))

final = CompositeVideoClip(layers, size=(W, H)).with_duration(total)

os.makedirs("assets", exist_ok=True)
final.write_videofile("assets/showcase.mp4", fps=OUT_FPS, codec="libx264", audio=False, logger=None)
print(f"Wrote assets/showcase.mp4 ({os.path.getsize('assets/showcase.mp4') / 1e6:.1f} MB, {total:.0f} s)")

small = final.resized(width=GIF_WIDTH)
small.write_gif("assets/showcase.gif", fps=GIF_FPS, logger=None)
print(f"Wrote assets/showcase.gif ({os.path.getsize('assets/showcase.gif') / 1e6:.1f} MB)")
final.close()
