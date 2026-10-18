"""Steps 5 and 6: same training as train.py, but with a custom reward wrapper.

Choose the reward on the command line:
    python train_wrapped.py time_penalty   # step 5 (default)
    python train_wrapped.py hover_hack     # step 6, the deliberate mistake
    python train_wrapped.py improvement_fix  # step 6, the fix

Add a seed as a second argument to repeat a run with different randomness:
    python train_wrapped.py hover_hack 1   # saves models/ppo_hover_hack_seed1.zip
Seed 0 is the original run and keeps the original file names.
"""
import os
import sys
import time

from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

from reward_wrapper import (
    HoverBonusWrapper,
    ImprovementBonusWrapper,
    TimePenaltyWrapper,
)

RUNS = {
    "time_penalty": (TimePenaltyWrapper, {"penalty": 0.05}),
    "hover_hack": (HoverBonusWrapper, {"bonus": 1.0}),
    "improvement_fix": (
        ImprovementBonusWrapper,
        {"scale": 5.0, "fee": 0.05, "gamma": 0.999},
    ),
}
choice = sys.argv[1] if len(sys.argv) > 1 else "time_penalty"
if choice not in RUNS:
    sys.exit(f"Unknown reward '{choice}'. Choose from: {', '.join(RUNS)}")
WRAPPER, WRAPPER_KWARGS = RUNS[choice]
SEED = int(sys.argv[2]) if len(sys.argv) > 2 else 0   # same settings as the baseline
RUN_NAME = f"ppo_{choice}" if SEED == 0 else f"ppo_{choice}_seed{SEED}"

TOTAL_STEPS = 1_000_000
N_ENVS = 16

os.makedirs("models", exist_ok=True)

env = make_vec_env(
    "LunarLander-v3",
    n_envs=N_ENVS,
    seed=SEED,
    wrapper_class=WRAPPER,
    wrapper_kwargs=WRAPPER_KWARGS,
)

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
    device="cpu",
    verbose=1,
)

start = time.time()
model.learn(total_timesteps=TOTAL_STEPS)
minutes = (time.time() - start) / 60
print(f"\nTraining took {minutes:.1f} minutes")

model.save(f"models/{RUN_NAME}")
print(f"Saved to models/{RUN_NAME}.zip")

env.close()
