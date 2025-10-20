from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from typing import Literal, Sequence

BaseName = Literal["uniform","normal"]

@dataclass
class PolyaSequenceModel:
    """Blackwell–MacQueen Pólya urn, base G0 ∈ {Uniform(0,1), Normal(0,1)}."""
    alpha: float = 5.0
    base: BaseName = "uniform"
    rng: np.random.Generator | None = None

    def _rng(self) -> np.random.Generator:
        return self.rng or np.random.default_rng()

    # base draw
    def P0(self) -> float:
        r = self._rng()
        if self.base == "uniform":
            return float(r.random())
        elif self.base == "normal":
            return float(r.standard_normal())
        raise ValueError(f"unknown base={self.base}")

    # one-step predictive given past x_{1:n}
    def Pn(self, n: int, history: Sequence[float]) -> float:
        r = self._rng()
        if n != len(history):
            raise ValueError("n must equal len(history)")
        w_base = self.alpha / (self.alpha + n)
        if r.random() < w_base:
            return self.P0()
        # sample a past value uniformly
        j = r.integers(0, n)
        return float(history[j])

# ----- small helpers used by both CLIs -----

def build_prefix(n_obs: int, model: PolyaSequenceModel) -> list[float]:
    """Generate x_{1:n_obs} from the urn."""
    x = [model.P0()]
    for m in range(1, n_obs):
        x.append(model.Pn(m, x))
    return x

def continue_urn_once(prefix: list[float], model: PolyaSequenceModel, M: int) -> list[float]:
    """Fix x_{1:n} and continue to length M using the predictive."""
    x = list(prefix)
    n = len(x)
    for m in range(n, M):
        x.append(model.Pn(m, x))
    return x

def sample_prior_once(M: int, model: PolyaSequenceModel) -> list[float]:
    """Unconditional Pólya sequence of length M."""
    x = [model.P0()]
    for m in range(1, M):
        x.append(model.Pn(m, x))
    return x
