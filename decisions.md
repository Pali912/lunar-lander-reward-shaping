# Decision Log

Every decision on this project goes here, newest at the bottom. Entries are never deleted. If a decision changes, add a new entry that marks the old one as **Superseded**.

**Entry template**

```
## D-XXX: Short title
- **Date:** YYYY-MM-DD
- **Status:** Accepted | Superseded by D-XXX | Reverted
- **Decision:** what we chose
- **Why:** the reasoning
- **Alternatives considered:** what we didn't pick
- **Consequences / follow-ups:** what this affects
```

---

## D-001: Keep project memory in two markdown files
- **Date:** 2026-10-17
- **Status:** Accepted
- **Decision:** `project.md` holds the project state (goal, plan, concepts, status, open questions). `decisions.md` holds every decision made.
- **Why:** So context survives between sessions and nothing gets re-debated or forgotten.
- **Alternatives considered:** A single combined file (decisions would get buried in project notes).
- **Consequences / follow-ups:** Update `project.md` as work progresses, and add a `decisions.md` entry whenever a choice is made.

## D-002: Base the project on Hari's Lunar Lander reward shaping doc
- **Date:** 2026-10-17
- **Status:** Accepted
- **Decision:** Follow the doc's plan: Gymnasium `LunarLander-v3`, Stable-Baselines3 PPO with `MlpPolicy`, custom reward wrapper, deliberate reward hacking experiment, then fix.
- **Why:** It's a complete, laptop-friendly plan with a clear success metric (average score of 200 or more, evaluated with the wrapper off over at least 10 attempts) and a resume-ready outcome.
- **Alternatives considered:** None discussed yet.
- **Consequences / follow-ups:** Use v3 not v2 everywhere. Open questions in `project.md` section 7 still need answers.

## D-003: Build on a Windows laptop using VS Code, working step by step
- **Date:** 2026-10-17
- **Status:** Accepted
- **Decision:** Develop and train locally on a Windows laptop, editing and running in VS Code (PowerShell terminal). Work through the 6 build steps one at a time, confirming each works before moving on.
- **Why:** Matches the doc's "free, laptop, no GPU" approach, and the person already has this setup. Going step by step keeps problems easy to isolate.
- **Alternatives considered:** Google Colab for training (kept as a fallback if local training is too slow).
- **Consequences / follow-ups:** Windows-specific install notes apply (Box2D build can need swig and the Microsoft C++ Build Tools). Commands use PowerShell syntax.

## D-004: Python 3.11 in a project-local virtual environment
- **Date:** 2026-10-17
- **Status:** Accepted
- **Decision:** Project lives at `E:\lunar-lander` with a virtual environment in `.venv` built on Python 3.11. Installed versions: gymnasium 1.4.0, stable-baselines3 2.9.0, torch 2.14.1, box2d 2.3.10, numpy 2.4.6, pygame-ce 2.5.8.
- **Why:** 3.11 is within the doc's 3.10+ requirement and the safest for the Box2D install. A venv keeps this project's packages separate from everything else. The install succeeded with no compiler issues, and the import check passed.
- **Alternatives considered:** Python 3.10 (also installed, not needed).
- **Consequences / follow-ups:** Activate with `.venv\Scripts\Activate.ps1` in each new terminal. Record the exact versions in `requirements.txt` for the GitHub repo. Gymnasium 1.4.0 only has `LunarLander-v3`, as the doc says.

## D-005: Track the project in Git and publish it to GitHub
- **Date:** 2026-10-17
- **Status:** Accepted
- **Decision:** Version the project with Git and push it to a GitHub repo. Commit `project.md`, `decisions.md`, `requirements.txt`, scripts, the reward wrapper, a README and short GIF clips. Ignore `.venv`, saved models (`*.zip`), large videos (`*.mp4`) and training logs via `.gitignore`.
- **Why:** The reward code and clips are the resume part of the project, and the decision log shows the thinking over time. Setting this up before training keeps big or throwaway files out of the history from the first commit.
- **Alternatives considered:** Keeping the project local only. Committing models and videos directly (bloats the repo).
- **Consequences / follow-ups:** Longer videos go in GitHub Releases or as links. Repo name and visibility decided in D-006.

## D-006: GitHub repo named `lunar-lander-reward-shaping`
- **Date:** 2026-10-17
- **Status:** Accepted
- **Decision:** Publish the project at https://github.com/Pali912/lunar-lander-reward-shaping. The local folder stays `E:\lunar-lander`, the names don't need to match. Visibility still to be confirmed (public recommended, since the reward code and clips are the showpiece).
- **Why:** The name says what the project is and what is interesting about it, which helps when someone skims the GitHub profile. Lowercase with hyphens follows GitHub convention.
- **Alternatives considered:** `rl-lunar-lander-ppo`, `reward-hacking-lunar-lander`, plain `lunar-lander` (too generic).
- **Consequences / follow-ups:** Repo was meant to be created empty (no README or .gitignore from GitHub) so the first push from the local folder does not conflict. Next: first commit and push.

## D-007: Git repo rooted in `E:\lunar-lander`, history rebased on GitHub's README commit
- **Date:** 2026-10-17
- **Status:** Accepted
- **Decision:** The Git repo for this project lives in `E:\lunar-lander` (`git init -b main`) and tracks `origin` at the GitHub repo from D-006. GitHub's auto-created `README.md` commit was brought in with `git pull --rebase origin main` before the first push, so history is a straight line. Git identity is set globally to the GitHub username `Pali912` with the email on the GitHub account (email deliberately not written in this file, the repo is public).
- **Why:** A stray empty repo already existed at `E:\` (no commits, no remote), so the first `git add .` tried to stage the whole `.venv`. Creating a repo inside the project folder fixed the root. The push was first rejected because GitHub's README commit existed remotely. Rebasing was safe because the local commit had not been pushed. The first commit was made under the correct email, so nothing needed rewriting.
- **Alternatives considered:** Force-pushing (would have deleted GitHub's README commit, rejected). Merge commit instead of rebase (works, but adds a needless merge). Deleting the repo at `E:\` right away (held off, asked first).
- **Consequences / follow-ups:** `.gitignore` must exist before the first `git add .` in any new repo. Check `git status` before every first commit. The empty repo at `E:\.git` still exists and should be removed later, with explicit OK, so other folders on that drive don't land inside it. The README from GitHub is a placeholder and should be replaced with a real one. Never put personal info (emails, keys) in these files, they are public.

## D-008: Claude maintains the notes files, they go into the repo at the end
- **Date:** 2026-10-17
- **Status:** Accepted
- **Decision:** `project.md` and `decisions.md` are kept up to date by Claude on its side as the work happens. They are not re-sent after every change. The finished versions get added to the GitHub repo when the project is complete.
- **Why:** Less file shuffling during the build, and the person can focus on the steps. Notes still capture every decision as it is made.
- **Alternatives considered:** Re-sending and committing after each change (what we did through D-007, more overhead).
- **Consequences / follow-ups:** The copies already committed to the repo are out of date until the final upload. Ask for the final versions at project completion.

## D-009: Baseline training config for step 3
- **Date:** 2026-10-17
- **Status:** Accepted (adjust if training does not reach 200 average)
- **Decision:** Train PPO with `MlpPolicy` for 1,000,000 steps on 16 parallel `LunarLander-v3` environments, seed 0, on CPU. Hyperparameters: `n_steps=1024`, `batch_size=64`, `n_epochs=4`, `gamma=0.999`, `gae_lambda=0.98`, `ent_coef=0.01`. Model saved to `models/ppo_baseline.zip` (git-ignored).
- **Why:** These are the values I recall from the Hugging Face Deep RL course Unit 1 for this game, chosen because they are known to reach the solved threshold more reliably than library defaults. Not verified against the course page, so treat as a reasoned starting point. CPU because the network is tiny.
- **Alternatives considered:** Plain PPO defaults on one environment (the doc's minimal description, may fall short of 200 at 1M steps).
- **Consequences / follow-ups:** This baseline is what the custom-reward runs in steps 5 and 6 get compared against. Same seed and settings for fair comparison. Record the training time in the progress log.

## D-010: Evaluation protocol for judging any model
- **Date:** 2026-10-18
- **Status:** Accepted
- **Decision:** A model's score is the mean over 20 attempts on the plain `LunarLander-v3` (custom reward wrapper off), using deterministic actions, run with `python play.py eval`. Solved means a mean of 200 or more. Watch and record runs use the same deterministic policy. Videos go to `videos/` (git-ignored), short GIFs for the repo get made later.
- **Why:** The doc requires at least 10 attempts with the wrapper off so a custom bonus can't flatter the result. 20 attempts gives a steadier average than 10, and costs seconds. Deterministic actions measure what the learned policy actually does without random exploration.
- **Alternatives considered:** Using the training `ep_rew_mean` as the score (it comes from the training environment, with exploration noise, and from the wrapped reward in later steps, so it is not comparable).
- **Consequences / follow-ups:** The same command must be used for the baseline and every custom-reward run so numbers are comparable. One seed is still one run, so important claims need more than one training run (doc's "trusting one run" pitfall).

## D-011: First custom reward is a 0.05 per-frame time charge
- **Date:** 2026-10-18
- **Status:** Accepted (value is a starting guess, tune if needed)
- **Decision:** Step 5's custom reward is `TimePenaltyWrapper`, which subtracts 0.05 from the reward every frame. Lives in `reward_wrapper.py`, trained by `train_wrapped.py` with the same seed, 16 envs, 1M steps and hyperparameters as the baseline (D-009). Model saved as `models/ppo_time_penalty.zip`. Evaluated with `python play.py eval models/ppo_time_penalty` (D-010, wrapper off).
- **Why:** The doc says start with a tiny per-frame charge for taking too long, since the built-in reward has none, then confirm the rocket still lands. 0.05 is small next to the +100/-100 landing and crash terms (a 250-frame landing pays about 12.5), but not zero, so waiting does cost something. Changing only one thing versus the baseline keeps the comparison clean. Original reward is stored in `info["base_reward"]`.
- **Alternatives considered:** 0.01 (almost no effect), 0.1 or more (risks teaching the rocket to rush into the ground to stop paying).
- **Consequences / follow-ups:** In SB3's `make_vec_env` the Monitor wrapper is applied before `wrapper_class`, so training's `ep_rew_mean` shows the original built-in score, not the wrapped one. Good for comparing against the baseline, but in step 6 it will not show the inflated hover reward, so hacking has to be confirmed from videos and from episode length. If the landing score drops well below the baseline, lower the penalty.

## D-012: Eval also reports score spread and attempt length
- **Date:** 2026-10-18
- **Status:** Accepted
- **Decision:** `python play.py eval` now prints, besides the mean and standard deviation over 20 attempts, the lowest and highest score, how many attempts scored under 200, and the mean attempt length in frames. The eval env is wrapped in `Monitor`, which also removes SB3's warning. The pass mark (mean of 200 or more) from D-010 is unchanged.
- **Why:** The step 5 training table showed `ep_len_mean` 908 (near the 1000 frame cap) while eval scored 262, and attempt length is the signal that separates a real landing from hovering, which step 6 depends on. A mean alone can also hide a few bad attempts.
- **Alternatives considered:** Judging only by the mean score (blind to hovering and to outliers).
- **Consequences / follow-ups:** Baseline and time penalty models must be re-evaluated with the new script so lengths can be compared. Length is the main hover detector for step 6.

## D-013: Eval uses fixed seeds so models are compared on the same starts
- **Date:** 2026-10-18
- **Status:** Accepted (amends how D-010 and D-012 are implemented)
- **Decision:** `python play.py eval` runs its own loop over 20 attempts, resetting attempt `i` with seed `1000 + i`, deterministic actions, wrapper off. It no longer uses SB3's `evaluate_policy` or `Monitor`. Reported: mean, std, lowest, highest, count under 200, mean attempt length.
- **Why:** The unseeded eval gave different numbers for unchanged models (baseline 241.5 then 244.4, time penalty 262.4 then 249.6), so score gaps under about 20 points were not trustworthy. Fixed seeds make a model's eval repeatable and put every model on identical starting conditions.
- **Alternatives considered:** Unseeded eval with more attempts (smoother but still not repeatable). Keeping `evaluate_policy` and seeding only the first reset (repeatable per model, but different models would see different starts).
- **Consequences / follow-ups:** Numbers from before this change are not comparable to numbers after it. Re-run baseline and time penalty for the official comparison. This does not remove seed-to-seed training variance, a model trained with another seed can still score differently.

## D-014: Step 6 hack design (hover bonus on its own, no time penalty)
- **Date:** 2026-10-18
- **Status:** Accepted
- **Decision:** The deliberate mistake is `HoverBonusWrapper`: +1 reward every frame the rocket is "upright and slow", defined by `is_upright_and_slow(obs)` as `abs(tilt) < 0.2`, `abs(x_speed) < 0.3` and `abs(y_speed) < 0.3` (normalized observation units, my own thresholds, the doc does not specify them). It is applied on top of the plain built-in reward, **without** the time penalty from D-011, so the baseline is the only comparison point and any change in behavior is caused by the bonus alone. Trained with `python train_wrapped.py hover_hack` (seed 0, same settings as D-009), saved as `models/ppo_hover_hack.zip`. `play.py eval` now also prints mean frames upright and slow, computed the same way for every model.
- **Why:** Matches the doc's reward-hacking example (+1 per frame, 1000-frame cap, landing ends the attempt). With a payment of up to 1000 against at most about 300 in fuel, staying up beats landing. Stacking the time penalty (0.05) would barely change that, but it would blur which change caused what. The doc's fix reintroduces a per-frame fee, which implies the broken version has none.
- **Alternatives considered:** Hack plus time penalty together (cleaner story only if it fails to hack). Stricter or looser thresholds (a looser "slow" makes the bonus easy to collect while falling, a stricter one makes it hard to find).
- **Consequences / follow-ups:** Training `ep_rew_mean` shows the original built-in score (Monitor sits inside the wrapper, see D-011), so it will not show the inflated reward. Hacking is judged from three signals: mean attempt length near the 1000 cap, a low true score, and a high "frames upright and slow" count, plus the video. The learned behavior may be hovering in the air or sitting on the ground firing small engine pulses to keep the lander awake, both are hacks. The doc says the hack may need a retrain or two to show up, so a different seed may be needed.
- **Outcome (added 2026-10-18):** The hack appeared on the first run with seed 0, no retrain needed. Seeded eval of `ppo_hover_hack`: true score -25.8 +/- 19.8, all 20 attempts ran the full 1000 frames, 963 frames on average upright and slow.
- **Correction (added 2026-10-18):** The "frames upright and slow" count turned out not to detect hovering on its own. A normal landing already scores 348 of 387 frames (baseline), because a calm descent counts. The hack's 963 of 1000 is only slightly higher as a share. The decisive hover signals are the 1000-frame attempt length and the true score of -25.8. The count is still useful for estimating the score the AI was chasing (true score plus bonus frames: about 600 for a baseline landing versus about 937 for the hover).
- **Behavior found (added 2026-10-18):** `play.py diagnose` shows the hack hovers in the air, it does not sit on the ground. Over five seeded attempts: 1000 frames each, legs on the ground 0% of the time, an engine firing on 99 to 100% of frames, average height 0.67 to 0.95. The baseline lands: 353 to 425 frames, legs down 11 to 14%, engines firing 68 to 72%, average height 0.55 to 0.66.

## D-015: The fix pays for improvement and adds a per-frame fee
- **Date:** 2026-10-18
- **Status:** Accepted (untested until trained)
- **Decision:** `ImprovementBonusWrapper` replaces the hover bonus. A frame is in the zone (1) or not (0), using the same `is_upright_and_slow` test as D-014. Each frame adds `5.0 * (0.999 * zone_now - zone_before) - 0.05` to the built-in reward. Entering the zone pays once, staying in it pays nothing, leaving it costs the same amount back. The 0.999 matches PPO's gamma so that sitting in the zone is a very small net cost, not a gain. Fee is 0.05 per frame, the same value as D-011. Trained with `python train_wrapped.py improvement_fix` (seed 0, same settings as D-009), saved as `models/ppo_improvement_fix.zip`.
- **Why:** The doc's fix: pay for getting better (the change between frames, like the built-in score does) instead of for sitting in a nice spot, and add a small fee every frame so waiting costs something. The hover bonus was a payment per frame in a state, which is exactly what could be farmed. Reusing the same zone definition keeps the before/after comparison fair. The scale of 5 is a starting guess.
- **Alternatives considered:** A smooth measure of how good the pose is instead of a 0/1 zone (more signal, more to tune). Scale 1 (may be too weak to matter), scale 20 or more (could drown out the built-in landing signal).
- **Consequences / follow-ups:** Must be evaluated the same way as every other model (D-010, D-013). Success means a mean score back near the baseline (about 250), attempt length well under 1000, and frames upright and slow in line with a real landing. If it fails to land, adjust the scale or the fee, and log the change. If it works on seed 0 only, that is one run, so a second seed is worth running before claiming the fix works.
- **Outcome (added 2026-10-18):** Worked on seed 0 without tuning. Seeded eval of `ppo_improvement_fix`: 237.7 +/- 21.6, lowest 205.6, no attempt under 200, mean length 431 frames, mean 370 frames upright and slow. The scale of 5 and fee of 0.05 stayed as first chosen. Still a single seed.

## D-016: Repeat baseline, hack and fix with training seed 1
- **Date:** 2026-10-18
- **Status:** Accepted
- **Decision:** Retrain the baseline, the hover hack and the improvement fix with training seed 1, all other settings unchanged (D-009). `train.py` and `train_wrapped.py` take the seed as an optional argument (`python train.py 1`, `python train_wrapped.py hover_hack 1`). Seed 0 keeps the original file names, other seeds get a `_seed1` style suffix, so nothing from the first runs is overwritten. Evaluated with the same seeded eval as before (D-013, start seeds 1000-1019), so only the training randomness differs. The time penalty model is not repeated, it is not part of the hack and fix story.
- **Why:** Everything so far is one training run per reward, and the doc warns against trusting one run. A second seed for all three models shows whether the hover and the fix repeat, and gives the baseline a second reference point so the fix is not judged against one lucky or unlucky run. Cost is about an hour of laptop time that can overlap with writing the GIFs and README.
- **Alternatives considered:** Only the hack and the fix on seed 1 (about 40 min, but then the baseline has one seed only). More than one extra seed (stronger, but the hour each is not worth it for this project). Skipping it (the story already holds on seed 0, but one run is easy to dismiss).
- **Consequences / follow-ups:** Report results as seed 0 and seed 1 side by side in the README. If the hack does not show up on seed 1, say so honestly, the doc says it may take a retrain or two to appear. Model files and results to be logged when the runs finish.
- **Outcome (added 2026-10-18):** Seed 1 repeated the seed 0 pattern for all three. Seeded eval: baseline 259.4 +/- 54.4 (lowest 37.9, 1 attempt under 200, 304 frames, 204 upright and slow), hover hack -80.3 +/- 23.8 (lowest -118.9, highest -44.7, 20 of 20 under 200, 1000 frames every attempt, 960 upright and slow), fix 266.0 +/- 21.7 (lowest 227.1, highest 306.2, 0 under 200, 311 frames, 233 upright and slow). The hover shows up on both seeds and the fix recovers a normal landing on both. The fix minus baseline gap changes sign between seeds (-12.7 on seed 0, +6.6 on seed 1), so there is no evidence the fix is better or worse than the baseline. The hack's true score differs a lot between seeds (-25.8 and -80.3), the hover is robust but how bad the score gets is not. Seed 1 hack behavior (hovering in the air) was inferred from length and the upright count, not checked with `diagnose`. Two seeds is still a small sample.

## D-017: README clips are short GIFs made from the seed 0 recordings
- **Date:** 2026-10-18
- **Status:** Accepted
- **Decision:** `make_gifs.py` converts the first recorded attempt of three seed 0 models (baseline, hover hack, improvement fix) into GIFs in `assets/`, limited to the first 12 seconds, 400 px wide, 15 frames per second. The GIFs are committed to the repo, the `.mp4` files stay ignored (D-005).
- **Why:** GIFs show inline on GitHub with no extra hosting, and the three clips tell the whole story side by side. Trimming and shrinking keeps each file small. The first 12 seconds of the hack clip already show it hanging in the air, the full 20 seconds adds nothing.
- **Alternatives considered:** Full length `.mp4` files in the repo (large and ignored by `.gitignore`), GitHub Releases or a video link (extra steps, no inline preview), seed 1 clips (no clips recorded for them yet).
- **Consequences / follow-ups:** Check the GIF file sizes, if any is above about 10 MB lower the width or frame rate. A GIF shows one attempt, the README should say the numbers come from the 20-attempt evals, not from the clip.

## D-018: README reports both seeds, states its limits, and credits the source
- **Date:** 2026-10-18
- **Status:** Accepted
- **Decision:** The repo's `README.md` leads with the three GIFs, then a results table with every evaluated model and seed (baseline, hover hack and fix on seeds 0 and 1, time penalty on seed 0), a plain explanation of the hack and the fix, the reward rules, reproduce steps for Windows PowerShell, a limits section, and a file list. It credits Hari's tutorial. It does not hide or smooth over weaker numbers (the baseline seed 1 outlier of 37.9 is in the table).
- **Why:** The README is the first thing a reader of the repo sees, and the project's value is an honest result, not a perfect one. Listing both seeds, the unverified hyperparameters, the guessed thresholds and the unchecked seed 1 hover keeps the claims inside what the data supports. Crediting the source is the right thing for a project built from someone else's tutorial.
- **Alternatives considered:** Showing only seed 0 (simpler, but hides that the result was repeated, or could have failed to repeat). A shorter README without limits (reads cleaner, claims more than the evidence).
- **Consequences / follow-ups:** If more seeds or a `diagnose` run on seed 1 are done later, update the results table and the limits section. The README says models and videos are not in the repo, which depends on `.gitignore` from D-005. The README credits Hari by name and handle (@harixganesh) with no link, because only the document was shared, not its URL, and the document does not say which platform the handle belongs to. Add a link if the original URL turns up.

## D-019: Side-by-side showcase video and sharper GIFs
- **Date:** 2026-10-18
- **Status:** Accepted (tested on synthetic clips of the same size, not yet on the real recordings)
- **Decision:** Add `make_showcase.py`, which places the three recorded seed 0 clips (baseline, hover hack, fix) side by side in 540 x 360 panels with a colored title, a one-line description of the reward rule, and the 20-attempt average underneath. Capped at 14 seconds, shorter clips hold their last frame. Outputs `assets/showcase.mp4` (30 fps) and `assets/showcase.gif` (900 px wide, 12 fps). Also raise `make_gifs.py` from 400 px and 15 fps to 600 px and 25 fps.
- **Why:** The person compared the repo clips with Hari's produced explainer video (a rendered 3D rocket, hand-drawn animations, subtitles) and found theirs poor looking. Two causes: Gymnasium draws flat shapes on a fixed 600 x 400 canvas, and D-017's GIFs were shrunk to 400 px at 15 fps, which blurred them further. Labels make each clip explain itself without the README, and native resolution removes the extra blur. The 3D look cannot come from the simulator's own renderer.
- **Alternatives considered:** Re-drawing the recorded states in a 3D engine, or editing a produced explainer with drawn animation and subtitles in a video editor (much more work, outside the scope of this project, possible later). Looping the short clips instead of holding the last frame (looks like repeated attempts).
- **Consequences / follow-ups:** Checked on three synthetic test clips: layout correct, no clipped text, mp4 1.2 MB, GIF 3.8 MB. Real clips have more detail, so the GIF may come out larger, lower `GIF_WIDTH` if it passes about 10 MB. The result lines in the labels are hard-coded from the seed 0 evals (250, -26, 238 and the frame counts), update them if models are retrained. GitHub shows the GIF inline in a README but not a relative `.mp4`, so the GIF goes in the README and the mp4 is for sharing elsewhere. README still embeds the three separate GIFs, switch to the showcase after the person has seen it.
- **Outcome (added 2026-10-18):** Ran on the real recordings. `assets/showcase.mp4` 0.2 MB (14 s), `assets/showcase.gif` 2.0 MB, and the separate GIFs at the new settings are 0.9 MB (baseline), 1.5 MB (hover hack) and 0.9 MB (fix). All well under the 10 MB limit, no resizing needed. What the clips look like on the real footage has not been reported back yet.

## D-020: README uses the showcase GIF, and showcase.mp4 is committed
- **Date:** 2026-10-18
- **Status:** Accepted
- **Decision:** The README's top section now embeds `assets/showcase.gif` instead of a table of three separate GIFs, and links `assets/showcase.mp4`. The separate GIFs stay in `assets/` and are mentioned in one sentence. `.gitignore` gets an exception, `!assets/*.mp4`, so the small showcase video is tracked while all other `.mp4` files (the raw recordings in `videos/`) stay ignored. README file list and reproduce steps mention `make_showcase.py`.
- **Why:** One labeled side-by-side clip says more than three small ones, and it is the first thing a visitor sees. The earlier `*.mp4` rule from D-005 would have silently skipped `showcase.mp4`, which is only 0.2 MB and worth keeping for sharing.
- **Alternatives considered:** Keeping the three-GIF table (redundant next to the showcase), dropping the mp4 from the repo (loses the better-quality version), un-ignoring all mp4 files (would commit large raw recordings).
- **Consequences / follow-ups:** The `.gitignore` exception must be in place before `git add`, or the mp4 is skipped. Commit and push are still pending.
