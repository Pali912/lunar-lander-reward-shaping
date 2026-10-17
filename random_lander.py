import gymnasium as gym

env = gym.make("LunarLander-v3", render_mode="human")
obs, info = env.reset(seed=42)

for step in range(500):
    action = env.action_space.sample()  # a random action
    obs, reward, terminated, truncated, info = env.step(action)

    if step % 25 == 0:
        print(f"step {step:3d} | reward {reward:7.2f} | obs {obs.round(2)}")

    if terminated or truncated:
        print("Attempt ended, restarting\n")
        obs, info = env.reset()

env.close()