"""Custom reward rules, layered on top of LunarLander's built-in reward.

A wrapper sits between the game and PPO. Each step it takes the built-in
reward, changes it, and passes the new total on. The game code is untouched.
"""
import gymnasium as gym


def is_upright_and_slow(obs):
    """True when the rocket is nearly upright and moving slowly.

    obs = [x, y, x_speed, y_speed, tilt, spin, left_leg, right_leg]
    Used by the hover bonus below, and by play.py eval to count hovering frames.
    """
    return abs(obs[4]) < 0.2 and abs(obs[2]) < 0.3 and abs(obs[3]) < 0.3


class TimePenaltyWrapper(gym.Wrapper):
    """Step 5: subtract a small fixed charge every frame.

    The built-in reward has no cost for taking too long, so this makes
    every extra frame cost a little.
    """

    def __init__(self, env, penalty=0.05):
        super().__init__(env)
        self.penalty = penalty

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        info["base_reward"] = reward  # keep the original for debugging
        return obs, reward - self.penalty, terminated, truncated, info


class HoverBonusWrapper(gym.Wrapper):
    """Step 6, the deliberate mistake: +1 for every frame upright and slow.

    This pays for SITTING in a nice spot instead of for getting better, so
    staying alive beats landing (landing ends the attempt and stops the
    payments). Expect reward hacking.
    """

    def __init__(self, env, bonus=1.0):
        super().__init__(env)
        self.bonus = bonus

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        info["base_reward"] = reward
        if is_upright_and_slow(obs):
            reward += self.bonus
        return obs, reward, terminated, truncated, info


class ImprovementBonusWrapper(gym.Wrapper):
    """Step 6, the fix: pay for GETTING BETTER, not for sitting in a good spot.

    Each frame the rocket is either in the "upright and slow" zone (1) or not (0).
    The bonus is paid on the change between frames, like the built-in score does,
    so entering the zone pays once and staying in it pays nothing. A small fee
    every frame means waiting costs something.
    """

    def __init__(self, env, scale=5.0, fee=0.05, gamma=0.999):
        super().__init__(env)
        self.scale = scale
        self.fee = fee
        self.gamma = gamma  # matches PPO's gamma, so sitting still is never a net gain
        self._prev = 0.0

    def reset(self, **kwargs):
        obs, info = self.env.reset(**kwargs)
        self._prev = float(is_upright_and_slow(obs))
        return obs, info

    def step(self, action):
        obs, reward, terminated, truncated, info = self.env.step(action)
        now = float(is_upright_and_slow(obs))
        info["base_reward"] = reward
        reward += self.scale * (self.gamma * now - self._prev) - self.fee
        self._prev = now
        return obs, reward, terminated, truncated, info
