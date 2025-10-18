from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from typing import Any
from .interfaces import PredictiveMethod, PredictiveState, Array

@dataclass
class _ECDFState:
    buffer: np.ndarray
    count: int = 0

class EmpiricalPredictive(PredictiveMethod):
    """Running empirical CDF (ECDF) as a one-step predictive."""
    def __init__(self, max_n: int):
        self.max_n = int(max_n)

    def init_state(self, **kwargs: Any) -> PredictiveState:
        return _ECDFState(buffer=np.empty(self.max_n, dtype=float), count=0)

    def update(self, state: _ECDFState, x: float) -> _ECDFState:
        state.buffer[state.count] = x
        state.count += 1
        return state

    def cdf_est(self, state: _ECDFState, t: Array) -> Array:
        if state.count == 0:
            t = np.asarray(t)
            return np.full_like(t, 0.5, dtype=float) if t.ndim else 0.5
        xs = state.buffer[: state.count]
        t_arr = np.asarray(t)
        if t_arr.ndim:
            return (xs[:, None] <= t_arr[None, :]).mean(axis=0)
        else:
            return (xs <= t_arr).mean()

    def pdf_est(self, state: _ECDFState, x: Array) -> Array:
        x_arr = np.asarray(x)
        return np.full_like(x_arr, np.nan, dtype=float) if x_arr.ndim else np.nan
