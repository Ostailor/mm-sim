Agents — Codex Brief

This file is not a functional part of the code‑base.  Its sole purpose is to tell an automated code‑generation assistant (e.g. GitHub Copilot / OpenAI Codex) exactly what to do when it is invited to create or update source files in this repository.

Humans may skim; Codex must obey.

1. High‑Level Mission

Generate and maintain the code for a free‑to‑run market‑making simulator and reinforcement‑learning bot with the architecture sketched in README.md and docs/spec.md.  All components must:

Run with no paid APIs or cloud services.

Stay within licence‑compatible, open‑source dependencies.

Be reproducible on a vanilla laptop or a free Google Colab session.

When in doubt, prefer simplicity over cleverness.

2. Repository Map (expected state)

backend/       FastAPI server + order‑book core
worker/        Celery tasks (training jobs)
agent/         RL + baseline bots
frontend/      Svelte UI
tests/         PyTest suites
data/          Public ITCH samples + checkpoints
docs/          Design notes

If a folder is missing, Codex must create it with minimal scaffolding.

3. Coding Standards

Aspect

Requirement

Formatting

Run Black (line 88), ruff for linting.

Typing

Add from __future__ import annotations and Pyright‑friendly type hints.

Logging

Use loguru with sensible defaults; no print() except in quick scripts.

Config

Use pydantic.BaseSettings; environment variables over hard‑coding paths.

Data paths

Resolve via Path(__file__).parent / ".." / "data", never absolute.

Comments

Docstring each public function (NumPy style).

Codex must refuse to commit code that fails ruff check . or pytest -q.

4. Tasks & Priorities

Order‑Book Engine: Implement insert/modify/cancel/market matching with Numba JIT; expose a thin Python OO wrapper.

ITCH Parser: Convert sample NASDAQ TotalView‑ITCH 5.0 files to JSONL events.

Gym Environment: Wrap the engine + replay feed into a vectorisable gymnasium.Env with discrete actions (0 = both sides, 1 = bid, 2 = ask).

Baseline Agents: Random, FixedSpread, InventorySkew for unit tests.

PPO Learner: Policy network, advantage calc, mini‑batch update.

FastAPI: /sessions, /ws/replay/{id}, /train POST that queues Celery task.

Svelte UI: Real‑time heat‑map, inventory/PnL card, training dialogue.

CI: GitHub Actions workflow that lint‑tests‑builds Docker images.

Docs: Auto‑generate API reference (sphinx‑autodoc) into docs/api/.

Codex should tackle tasks in this order unless human commit messages override.

5. Unit‑Testing Expectations

Backend: ≥ 90 % coverage on order book and env logic.

Frontend: Minimal Jest + Testing‑Library smoke tests.

RL: Evaluate trained checkpoint over 5 episodes and assert mean PnL > 0.

Codex must add or update tests alongside all new code.

6. Training Constraints

CPU‑only training should finish 10 k steps in ≤ 5 min on a 4‑core laptop.

GPU code must auto‑detect CUDA and fall back gracefully.

7. Non‑Goals

No paid data feeds, exotic infra, or secret keys.

No third‑party ML hosting platforms.

No automatic front‑running or unethical trading features.

8. How to Ask for Human Help

If Codex encounters an ambiguous spec or missing dependency, it should:

Emit a TODO comment describing the uncertainty.

Generate a concise Git commit message prefixed with WIP:.

Await human review before proceeding.

End of Codex brief.

