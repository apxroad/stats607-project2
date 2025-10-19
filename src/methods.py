from __future__ import annotations

import numpy as np
from typing import Any
from .interfaces import PredictiveMethod, PredictiveState, Array
from .dgps import NormalTruth, UniformTruth

class PolyaPredictive(PredictiveMethod):
    r"""
    Dirichlet–process (Pólya sequence) one-step predictive for CDFs.

    For any threshold t and observed data x_{1:n}, with base G0 and concentration α>0,
        \tilde P_n((−∞, t]) = (α G0(t) + K_n(t)) / (α + n),
    where K_n(t) = \sum_{i=1}^n 1{x_i ≤ t}.

    Notes
    -----
    - This class estimates the **CDF**; `pdf_est` returns NaNs because the DP
      predictive has discrete atoms (not suitable for log-density scoring).
    - `base` controls the prior base CDF G0:
        * "normal"  → NormalTruth(mean=0, sd=1)
        * "uniform" → UniformTruth(a=0, b=1)
    """

    def __init__(self, alpha: float = 5.0, base: str = "normal"):
        assert alpha > 0, "alpha must be positive"
        self.alpha = float(alpha)
        if base == "normal":
            self.base = NormalTruth()
        elif base == "uniform":
            self.base = UniformTruth(0.0, 1.0)
        else:
            raise ValueError(f"Unknown base '{base}'. Use 'normal' or 'uniform'.")

    # ---- PredictiveMethod API ----
    def init_state(self, **kwargs: Any) -> PredictiveState:
        # Keep a simple list of observed values; order doesn't matter (exchangeable).
        return {"xs": []}

    def update(self, state: dict, x: float) -> dict:
        state["xs"].append(float(x))
        return state

    def cdf_est(self, state: dict, t: Array) -> Array:
        xs = np.asarray(state["xs"], dtype=float)
        n = xs.size
        t_arr = np.asarray(t, dtype=float)

        # counts K_n(t): number of observed x ≤ t 
        if n == 0:
            counts = 0.0
        else:
            counts = (
                (xs[:, None] <= t_arr[None, :]).sum(axis=0)
                if t_arr.ndim
                else (xs <= t_arr).sum()
            )

        g0 = self.base.cdf_truth(t_arr)
        return (self.alpha * g0 + counts) / (self.alpha + n)

    def pdf_est(self, state: dict, x: Array) -> Array:
        # DP predictive has discrete atoms; we leave density undefined for scoring.
        x_arr = np.asarray(x, dtype=float)
        return np.full_like(x_arr, np.nan, dtype=float) if getattr(x_arr, "ndim", 0) else np.nan
