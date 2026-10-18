# Project: Lunar Lander with Reward Shaping

**Source:** "Training an AI to land a rocket with reward shaping" by Hari (@harixganesh)
**Started:** 2026-10-17
**Status:** Build steps 1 to 6 complete, second seed done, GIFs and README written (2026-10-18). Pushed to GitHub (public). Remaining: remove the stray `gitignore` file from the repo, remove the stray `E:\.git` repo (needs explicit OK).
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
- [x] **2. Watch it fail (20 min). DONE 2026-10-17.** Create `LunarLander-v3` with the window on, send random actions in a reset/step loop. Print the 8 numbers and match them to the table.
- [x] **3. Train it (about 30 min of waiting). DONE 2026-10-18, training took 20.2 min.** PPO + `MlpPolicy`, 1M steps (HF course says about 20 min on Colab, so time mine). Watch `ep_rew_mean`, it should climb. Save the model.
- [x] **4. Watch it land and record (30 min). DONE 2026-10-18.** Load the model and fly it. Record with Gymnasium `RecordVideo` (needs `rgb_array` mode and `moviepy`) or the GIF example from the SB3 examples page.
- [x] **5. Write my own reward (a few hours). DONE 2026-10-18 (check passed, episode-length question open, see progress log).** Build a wrapper between the game and PPO: takes built-in reward, adds/subtracts my terms, passes the total on. Start with a tiny per-frame time charge (built-in has none), retrain, confirm it still lands.
- [x] **6. Break it, then fix it. DONE 2026-10-18 (one seed each, replication optional).** Add the "+1 per frame" rule, retrain, watch the clip not just the score (score can rise while the rocket hovers; may take a retrain or two to show). Apply the fix, retrain, keep both clips.

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
- ~~How many seeds/retrains per experiment before I trust a result?~~ Answered: two training seeds (0 and 1) for baseline, hack and fix (D-016). Small sample, enough to show the pattern repeats.

---

## 8. Progress log

| Date | Update |
|---|---|
| 2026-10-17 | Project created from Hari's doc. Created `project.md` and `decisions.md`. |
| 2026-10-17 | Environment chosen: Windows laptop + VS Code, local training (D-003). Starting step 1 (setup). |
| 2026-10-17 | Step 1 complete. Project at `E:\lunar-lander`, venv in `.venv` (Python 3.11), installed gymnasium 1.4.0, stable-baselines3 2.9.0, torch 2.14.1, box2d 2.3.10. Import check passed (D-004). Next: step 2, watch a random rocket crash. |
| 2026-10-17 | Saved `requirements.txt` (pip freeze). Step 2 complete: `random_lander.py` ran, random rocket crashed and restarted several times (attempts ended around 25 to 100 frames in). Observed the 8 numbers: starting height about 1.4 (doc's example used 0.9), leg flag 7 flipped to 1 when the left leg touched down. Next: Git/GitHub setup (D-005), then step 3 (train PPO). |
| 2026-10-17 | Created GitHub repo `Pali912/lunar-lander-reward-shaping` (D-006). Next: first commit and push, then step 3. |
| 2026-10-17 | First push to GitHub succeeded (D-007). Hit and fixed: stray empty repo at `E:\` (so `.venv` got staged, unstaged before any commit), missing `.gitignore`, push rejected over GitHub's README, wrong global git email. History is now `origin/main` with README plus our first commit. Next: commit the D-007 log, then step 3 (train PPO). |
| 2026-10-17 | Workflow change (D-008): notes kept on Claude's side, uploaded to repo at the end. Step 3 started: wrote `train.py` (D-009, baseline PPO, 16 envs, 1M steps, CPU). Waiting on first training run and its timing. |
| 2026-10-18 | Step 3 complete: `train.py` ran 1,015,808 timesteps (1M plus rollout rounding), 244 updates, took **20.2 minutes** on the laptop CPU. Model saved to `models/ppo_baseline.zip`. Final `ep_rew_mean` not yet seen (pasted output started after it), so the real score comes from the 20-attempt eval. Wrote `play.py` (eval, watch, record) for step 4 (D-010). |
| 2026-10-18 | **Baseline result (D-009 config, seed 0): mean score 241.5 +/- 37.6 over 20 attempts, SOLVED.** `play.py watch` 5 attempts scored 260.2, 262.4, 257.5, 293.1, 262.6. The SB3 "no Monitor wrapper" warning on eval is harmless here since no wrapper changes rewards. The spread (37.6) suggests a few weaker attempts in the 20. Still to do for step 4: record videos (`play.py record`, needs moviepy). This is the baseline for steps 5 and 6. |
| 2026-10-18 | Step 4 complete: installed moviepy 2.2.1, `play.py record` saved 3 baseline videos in `videos/` (scores 240.0, 231.6, 286.0). `requirements.txt` needs a refresh (`pip freeze`) because moviepy was added after it was written. Fixed `play.py` so video names use the model name (was hardcoded "baseline", would have overwritten the baseline clips). Step 5 started: wrote `reward_wrapper.py` (TimePenaltyWrapper) and `train_wrapped.py` (D-011). |
| 2026-10-18 | Step 5 run: `train_wrapped.py` (0.05 per frame time charge, seed 0) took **13.9 min** (baseline 20.2, cause unknown, probably laptop load). Eval with wrapper off: **262.4 +/- 20.5, SOLVED** (baseline 241.5 +/- 37.6). One seed each, so this does not prove the penalty helped. Last training table showed ep_rew_mean 150 and **ep_len_mean 908** (near the 1000 frame cap) with exploration noise on, versus 262 in deterministic eval. Odd given a penalty meant to shorten attempts, and I never saw the baseline's ep_len_mean. Upgraded `play.py eval` to also print lowest/highest score, count under 200 and mean attempt length (D-012). Next: run it on both models and compare lengths before step 6. |
| 2026-10-18 | Re-eval with the D-012 script (unseeded): baseline **244.4 +/- 38.4**, lowest 94.2, 1 attempt under 200, mean length **415** frames. Time penalty **249.6 +/- 24.4**, lowest 215.1, 0 under 200, mean length **335** frames. Penalty model is shorter, as intended, so the 908 ep_len_mean was training exploration, not a real behaviour (best guess, unconfirmed). Same models scored differently between the first and second eval (baseline 241.5 vs 244.4, penalty 262.4 vs 249.6): the unseeded eval is noisy, so earlier score gaps mean little. `play.py watch models/ppo_time_penalty` scores 285.0, 243.0, 264.0, 250.1, 266.6. Eval now uses fixed seeds 1000-1019 (D-013); both models need re-eval for the official comparison numbers. |
| 2026-10-18 | **Official seeded results (D-013, seeds 1000-1019, deterministic, wrapper off).** Baseline: **250.4 +/- 16.9**, lowest 218.4, highest 277.2, 0 under 200, mean length **387** frames. Time penalty: **258.0 +/- 19.5**, lowest 224.0, highest 290.8, 0 under 200, mean length **344** frames. Gap is 7.6 points on one seed each, not conclusive. Penalty is about 11% shorter, direction as intended. Step 6 started: added `HoverBonusWrapper` and `is_upright_and_slow()` to `reward_wrapper.py`, `train_wrapped.py` now takes a reward name argument (`time_penalty` or `hover_hack`), `play.py eval` also prints mean frames upright and slow (D-014). Next: train `hover_hack`, eval it, watch the clip. |
| 2026-10-18 | **Reward hacking confirmed on the first try.** `hover_hack` (+1 per frame upright and slow, seed 0) trained in **15.7 min**. Eval (seeded, wrapper off): true score **-25.8 +/- 19.8**, lowest -64.0, highest 9.4, **20 of 20 attempts under 200**, mean length **1000 frames (every attempt hit the cap)**, mean frames upright and slow **963**. The score the AI was optimizing is roughly true score plus bonus frames, about -25.8 + 963 = **937**, versus about 250 true plus a few hundred bonus frames for a real landing, so hovering paid far more than landing. Watch scores: -53.3, -60.7, -2.9, -53.1, -31.7. Built the fix, `ImprovementBonusWrapper` (D-015). Next: record the hover clip, train `improvement_fix`, eval, record the fixed clip. |
| 2026-10-18 | **Fix confirmed.** `improvement_fix` (5 x change in zone minus 0.05 per frame, seed 0) trained in **20.4 min**. Eval (seeded, wrapper off): **237.7 +/- 21.6**, lowest 205.6, highest 283.1, **0 under 200**, mean length **431** frames, mean frames upright and slow **370**. Hack went from 1000 frames and -25.8 to a normal landing. Compared with the baseline (250.4, 387 frames) the score is about 13 lower and attempts about 44 frames longer, small and within what one seed can produce. `play.py record` saved 3 fixed clips (scores 262.9, 274.9, 236.7), file prefix `ppo_improvement_fix`. Caveat: 370 of 431 frames count as upright and slow, so that metric also counts a calm controlled descent, it only means something next to the baseline's number, which has not been run yet. Gymnasium warned "Overwriting existing videos", it only warns when the folder has files, clips from other models have different file prefixes and are not overwritten. Still open: baseline and time-penalty values for frames upright and slow, confirm the hover clip exists, GIFs for the repo, real README, final upload of notes. |
| 2026-10-18 | Frames upright and slow filled in for the other models (same seeded eval): baseline **348** of 387 frames (90%), time penalty **283** of 344 (82%), fix **370** of 431 (86%), hover hack **963** of 1000 (96%). **Correction:** a normal landing already spends about 90% of its time upright and slow, so this count alone does not detect hovering. The real hover signals are attempt length at the 1000 cap and the very low true score. It does explain why the hack pays: the hacked score is roughly true score plus bonus frames, about 250 + 348 = 600 for a baseline landing versus about -26 + 963 = 937 for the hover, a margin of roughly 340 points. The fix's 370 is in line with the baseline's 348, as intended. |
| 2026-10-18 | Recorded the hover clip: `play.py record models/ppo_hover_hack` (scores -2.2, -53.2, -20.4, prefix `ppo_hover_hack`). What the rocket does in the clip is not known yet (cannot view the videos), so added `play.py diagnose` which prints per attempt the frames, share of frames with legs on the ground, share with an engine firing, and average height. Open: run it on the hack and on the baseline, decide on a second seed, GIFs, README, final notes upload. |
| 2026-10-18 | **Hack behavior identified** with `play.py diagnose` (seeded, 5 attempts). Hover hack: 1000 frames every attempt, legs on ground **0%**, engines firing **99 to 100%**, average height **0.67 to 0.95** (mean about 0.84). So it hovers in the air for the whole attempt, never landing. It does not sit on the ground. Baseline for contrast: 353 to 425 frames, legs on ground 11 to 14%, engines firing 68 to 72%, average height 0.55 to 0.66 (mean about 0.61). README line: with a +1 per frame upright-and-slow bonus the agent learned to hover for all 1000 frames and its true score fell from about 250 to about -26. Waiting on the person's choice: second seed for hack and fix (about 40 min) or go straight to GIFs, README and final notes upload. |
| 2026-10-18 | Next steps agreed in principle (D-016): run training seed 1 for baseline, hover hack and fix (about 1 hour, overlaps with other work), meanwhile make GIFs and the README. Added an optional seed argument to `train.py` and `train_wrapped.py` (seed 0 keeps original file names). Open: the seed 1 results, GIFs, README, final notes upload to the repo, remove the stray `E:\.git` repo (needs explicit OK). |
| 2026-10-18 | Seed 1 training finished for all three (D-016): baseline, hover hack and improvement fix run back to back in one command. Last table shown was `improvement_fix` seed 1: **16.6 min**, training `ep_rew_mean` **262** (original game score with exploration noise, not the eval number). Models saved as `ppo_baseline_seed1`, `ppo_hover_hack_seed1`, `ppo_improvement_fix_seed1`. Their timings for the first two were not shown. Next: seeded eval of all three and compare with seed 0. |
| 2026-10-18 | **Seed 1 results (seeded eval, wrapper off).** Baseline **259.4 +/- 54.4**, lowest 37.9, 1 under 200, **304** frames, 204 upright and slow. Hover hack **-80.3 +/- 23.8**, lowest -118.9, highest -44.7, 20 of 20 under 200, **1000** frames, 960 upright and slow. Fix **266.0 +/- 21.7**, lowest 227.1, highest 306.2, 0 under 200, **311** frames, 233 upright and slow. Same story as seed 0: hover appears on both seeds, fix lands again on both. Fix minus baseline is -12.7 on seed 0 and +6.6 on seed 1, so no real difference. Hacked score estimate on seed 1: about -80 + 960 = 880 for the hover versus about 259 + 204 = 463 for a baseline landing. Baseline seed 1 has one weak attempt (37.9) that inflates its spread. Seed 1 hover behavior not diagnosed. Wrote `make_gifs.py` (D-017). Next: make the GIFs, write the README, final notes upload. |
| 2026-10-18 | GIFs made with `make_gifs.py`: `assets/baseline.gif` 0.4 MB, `assets/hover_hack.gif` 0.7 MB, `assets/improvement_fix.gif` 0.4 MB, all small enough to commit. Wrote the real `README.md` (D-018): GIF table, both-seed results, what happened, reward rules, reproduce steps, limits, file list. Privacy check on `project.md` and `decisions.md` found no email addresses or real names. Final versions of both notes files, README and scripts handed over for the repo commit. Open: commit and push (include `assets/`, refresh `requirements.txt` with `pip freeze` first because moviepy was added), remove the stray `E:\.git` repo with explicit OK. |
| 2026-10-18 | The person shared Hari's explainer video (720 x 1280, 72 s: rendered 3D rocket with a SCORE board and a "RESUME PROJECT" label, hand-drawn whiteboard animations, subtitles) and said their own clips look poor. Cause: the simulator's flat 600 x 400 render, plus my GIFs shrunk to 400 px at 15 fps. Wrote `make_showcase.py` (labeled side-by-side video and GIF) and raised `make_gifs.py` to 600 px and 25 fps (D-019). Tested on synthetic clips only. Commit and push still pending, README still points at the three separate GIFs. |
| 2026-10-18 | Ran `make_showcase.py` and `make_gifs.py` on the real clips: showcase.mp4 0.2 MB, showcase.gif 2.0 MB, separate GIFs 0.9 / 1.5 / 0.9 MB. README now embeds the showcase GIF (D-020). `.gitignore` got `!assets/*.mp4` so the showcase video is tracked. Final files to hand over: `README.md`, `.gitignore`, `project.md`, `decisions.md`. Open: commit and push, remove the stray `E:\.git` repo with explicit OK. |
| 2026-10-18 | **Pushed to GitHub.** Checked the repo page logged out: it is **public**, 4 commits, README renders with the showcase GIF under "The three behaviors". Root has `assets/`, `.gitignore`, `README.md`, `decisions.md`, `make_gifs.py`, `make_showcase.py`, `play.py`, `project.md`, `random_lander.py`, `requirements.txt`, `reward_wrapper.py`, `train.py`, `train_wrapped.py`, plus a **stray file named `gitignore`** (no dot, probably a downloaded copy that `git add .` picked up) to remove with `git rm gitignore`. Could not list `assets/` (GitHub blocks that page for my tools), so the GIFs and `showcase.mp4` being there is unconfirmed. Notes in the repo are the versions at push time, later changes need another commit. Open: remove the stray `gitignore` file, remove the stray `E:\.git` repo with explicit OK. |
