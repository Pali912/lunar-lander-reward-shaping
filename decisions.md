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
