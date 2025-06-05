from __future__ import annotations

from backend.env import MarketEnv


def test_env_step() -> None:
    env = MarketEnv()
    obs, _ = env.reset()
    assert env.action_space.n == 3
    obs, reward, terminated, truncated, _ = env.step(0)
    assert obs.shape == (2,)
    assert isinstance(reward, float)
    assert not terminated
    assert not truncated
