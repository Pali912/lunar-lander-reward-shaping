"""Steps 4 to 6: score, watch and record a trained agent.

Usage (with the venv active):
    python play.py eval      # score over 20 fixed attempts, no window
    python play.py watch     # 5 attempts in a game window
    python play.py diagnose  # hovering or on the ground? per-attempt numbers
    python play.py record    # 3 attempts saved as videos in videos/
    python play.py record models/other_model   # use a different model
"""
import os
import sys

import gymnasium as gym
import numpy as np
from gymnasium.wrappers import RecordVideo
from stable_baselines3 import PPO

from reward_wrapper import is_upright_and_slow

mode = sys.argv[1] if len(sys.argv) > 1 else "eval"
model_path = sys.argv[2] if len(sys.argv) > 2 else "models/ppo_baseline"

model = PPO.load(model_path, device="cpu")


def fly(env, attempts):
    for i in range(attempts):
        obs, _ = env.reset()
        total, done = 0.0, False
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)
            total += reward
            done = terminated or truncated
        print(f"Attempt {i + 1}: score {total:.1f}")


if mode == "eval":
    env = gym.make("LunarLander-v3")
    scores, lengths, hover = [], [], []
    for i in range(20):
        # Fixed seed per attempt: every model faces the same 20 starting conditions
        obs, _ = env.reset(seed=1000 + i)
        total, steps, bonus, done = 0.0, 0, 0, False
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)
            total += reward
            steps += 1
            bonus += int(is_upright_and_slow(obs))
            done = terminated or truncated
        scores.append(total)
        lengths.append(steps)
        hover.append(bonus)
    mean = np.mean(scores)
    print(f"Mean score over 20 attempts: {mean:.1f} +/- {np.std(scores):.1f}")
    print(
        f"Lowest {np.min(scores):.1f}, highest {np.max(scores):.1f}, "
        f"attempts under 200: {int(np.sum(np.array(scores) < 200))}"
    )
    print(f"Mean attempt length: {np.mean(lengths):.0f} frames (cap is 1000)")
    print(
        f"Mean frames upright and slow: {np.mean(hover):.0f} "
        f"(a hover bonus of +1 per frame would add this to the score)"
    )
    print("SOLVED (200 or more)" if mean >= 200 else "Not solved yet (needs 200 or more)")
    env.close()

elif mode == "diagnose":
    # What is the rocket actually doing? Hovering in the air, or sitting on the ground?
    env = gym.make("LunarLander-v3")
    for i in range(5):
        obs, _ = env.reset(seed=1000 + i)
        steps, on_ground, firing, heights, done = 0, 0, 0, [], False
        while not done:
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, terminated, truncated, _ = env.step(action)
            steps += 1
            on_ground += int(obs[6] > 0.5 or obs[7] > 0.5)
            firing += int(action != 0)
            heights.append(obs[1])
            done = terminated or truncated
        print(
            f"Attempt {i + 1}: {steps} frames | legs on ground {100 * on_ground / steps:.0f}% "
            f"| engines firing {100 * firing / steps:.0f}% | average height {np.mean(heights):.2f}"
        )
    env.close()

elif mode == "watch":
    env = gym.make("LunarLander-v3", render_mode="human")
    fly(env, 5)
    env.close()

elif mode == "record":
    env = gym.make("LunarLander-v3", render_mode="rgb_array")
    env = RecordVideo(
        env,
        video_folder="videos",
        name_prefix=os.path.basename(model_path),
        episode_trigger=lambda i: True,
    )
    fly(env, 3)
    env.close()
    print("Videos saved in the videos folder")

else:
    print("Mode must be eval, diagnose, watch or record")
