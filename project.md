# Project: Lunar Lander with Reward Shaping

**Source:** "Training an AI to land a rocket with reward shaping" by Hari (@harixganesh)
**Started:** 2026-10-17
**Status:** Planning (nothing built yet)
**Companion file:** `decisions.md` (every decision goes there, with date and reasoning)

---

## 1. Goal

Train an AI (reinforcement learning, PPO) to land a rocket in Gymnasium's Lunar Lander, then design my own reward rules on top, break them on purpose (reward hacking), fix them, and record both results.

**Deliverables (the resume project):**
- A clip of the trained agent landing
- My reward wrapper code
- A clip of the "hover" failure (reward hacking)
- A clip/result after the fix

**Time budget:** about an afternoon for a first landing, the rest of the day for reward experiments. Free, runs on a laptop, no GPU needed. Needs basic Python (loops, functions, classes).

---

## 2. Core concepts (quick reference)

- **Reinforcement learning:** the AI tries thousands of landings, gets points for good behavior and penalties for bad. Like training a dog with treats, but the treats are points.
- **Reward shaping:** changing how points are awarded to steer behavior. This is the main experiment.
- **Environment:** Gymnasium `LunarLander-v3`, 50 frames per second (a frame is one physics tick).
- **Library stack:** Python 3.10+, Gymnasium (with `box2d` extra), Stable-Baselines3 (brings PyTorch).
- **Algorithm:** PPO (Proximal Policy Optimization, OpenAI 2017). Keeps each update small so one lucky stretch can't wreck learning.
- **Network:** `MlpPolicy`, two layers of 64 units, a few thousand weights. Provided by Stable-Baselines3.

### Observation (8 numbers per frame)
| # | Meaning | Example |
|---|---|---|
| 1 | left/right of pad | 0.20 (a bit right) |
| 2 | height above pad | 0.90 (high) |
| 3 | sideways speed | -0.10 (drifting left) |
| 4 | up/down speed | -0.50 (falling) |
| 5 | tilt (radians) | 0.05 (nearly upright) |
| 6 | spin speed | 0.00 |
| 7 | left leg on ground | 0 or 1 |
| 8 | right leg on ground | 0 or 1 |

The AI never sees the picture, only these numbers.

### Actions (one per frame)
Do nothing, fire left engine, fire main engine, fire right engine.

### Built-in reward
Each frame computes a position score: `-100*distance - 100*speed - 100*tilt + 10 per leg down`. Frame reward = improvement in that score since last frame, minus 0.3 if main engine fired, minus 0.03 if a side engine fired. Final frame: +100 for safe landing, -100 for crash. Sum over all frames is the episode score.

Worked example from the doc: score goes from -100 to -97 (improved by 3), main engine fired, so reward = 3 - 0.3 = 2.7.

### Reward hacking (the key lesson)
If I add "+1 per frame while upright and slow", episodes are capped at 1,000 frames, so hovering can collect up to 1,000 points against at most 300 in fuel cost. Landing ends the episode and stops the payments, so hovering beats landing and training can learn exactly that.

**Fix:** pay for *improvement* (change between frames, like the built-in score) instead of for sitting in a good spot, and add a small per-frame fee so waiting costs something.

---

## 3. Build plan

- [x] **1. Set up (under 1 hr). DONE 2026-10-17.** Python 3.10+, virtual environment, pip install Gymnasium with `box2d` extra and Stable-Baselines3. Done when Python imports all three without error.
- [ ] **2. Watch it fail (20 min).** Create `LunarLander-v3` with the window on, send random actions in a reset/step loop. Print the 8 numbers and match them to the table.
- [ ] **3. Train it (about 30 min of waiting).** PPO + `MlpPolicy`, 1M steps (HF course says about 20 min on Colab, so time mine). Watch `ep_rew_mean`, it should climb. Save the model.
- [ ] **4. Watch it land and record (30 min).** Load the model and fly it. Record with Gymnasium `RecordVideo` (needs `rgb_array` mode and `moviepy`) or the GIF example from the SB3 examples page.
- [ ] **5. Write my own reward (a few hours).** Build a wrapper between the game and PPO: takes built-in reward, adds/subtracts my terms, passes the total on. Start with a tiny per-frame time charge (built-in has none), retrain, confirm it still lands.
- [ ] **6. Break it, then fix it.** Add the "+1 per frame" rule, retrain, watch the clip not just the score (score can rise while the rocket hovers; may take a retrain or two to show). Apply the fix, retrain, keep both clips.

---

## 4. Success criteria

- One number: **average score over many attempts**. Solved = 200 or more.
- Evaluate with **my wrapper turned off**, over **at least 10 attempts**, so my own bonus can't flatter the result.
- The curve starts well below zero and wobbles on the way up. That's normal.
- Run more than once before calling a reward good or bad, training is random.

---

## 5. Known pitfalls

- Box2D install fails mentioning `swig`: install swig first, then the box2d extra again.
- Old tutorials say `LunarLander-v2`. Current Gymnasium only has **v3**. Change 2 to 3 (applies to the Hugging Face course too).
- Trusting a single run.
- Judging by score alone instead of watching the clip.

---

## 6. Resources (in this order)

1. Stable-Baselines3: Install
2. Gymnasium: Basic Usage (reset/step loop, on a different game)
3. Gymnasium: Lunar Lander (8 numbers, actions, reward)
4. Hugging Face Deep RL Course, Unit 1 (trains PPO on this game, uses v2, switch to v3)
5. Stable-Baselines3: Examples (training, saving, loading, GIFs)
6. Gymnasium: Implementing Custom Wrappers (use the plain `Wrapper` section)

Author asked to be sent the result if I build it: @harixganesh.

---

## 7. Open questions

- ~~Which machine and OS?~~ Answered: Windows laptop, VS Code (see D-003).
- ~~Local laptop or Colab for training?~~ Local for now, Colab as fallback (see D-003).
- What reward terms do I want to try beyond the time charge and the hover hack?
- How many seeds/retrains per experiment before I trust a result?

---

## 8. Progress log

| Date | Update |
|---|---|
| 2026-10-17 | Project created from Hari's doc. Created `project.md` and `decisions.md`. |
| 2026-10-17 | Environment chosen: Windows laptop + VS Code, local training (D-003). Starting step 1 (setup). |
| 2026-10-17 | Step 1 complete. Project at `E:\lunar-lander`, venv in `.venv` (Python 3.11), installed gymnasium 1.4.0, stable-baselines3 2.9.0, torch 2.14.1, box2d 2.3.10. Import check passed (D-004). Next: step 2, watch a random rocket crash. |
