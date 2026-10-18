"""Step 3: train a baseline PPO agent on LunarLander-v3 (no custom reward yet).

    python train.py        # seed 0, saves models/ppo_baseline.zip (the original run)
    python train.py 1      # seed 1, saves models/ppo_baseline_seed1.zip
"""
import os
import sys
import time

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

TOTAL_STEPS = 1_000_000
N_ENVS = 16          # 16 landers practice at once (same process, still just CPU)
SEED = int(sys.argv[1]) if len(sys.argv) > 1 else 0
RUN_NAME = "ppo_baseline" if SEED == 0 else f"ppo_baseline_seed{SEED}"

os.makedirs("models", exist_ok=True)

env = make_vec_env("LunarLander-v3", n_envs=N_ENVS, seed=SEED)

model = PPO(
    "MlpPolicy",
    env,
    n_steps=1024,
    batch_size=64,
    n_epochs=4,
    gamma=0.999,
    gae_lambda=0.98,
    ent_coef=0.01,
    seed=SEED,
    device="cpu",    # small network, CPU is faster than GPU here
    verbose=1,       # prints ep_rew_mean while training
)

start = time.time()
model.learn(total_timesteps=TOTAL_STEPS)
minutes = (time.time() - start) / 60
print(f"\nTraining took {minutes:.1f} minutes")

model.save(f"models/{RUN_NAME}")
print(f"Saved to models/{RUN_NAME}.zip")

env.close()
