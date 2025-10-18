# src/methods.py
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


from scipy.stats import norm, t  

@dataclass
class _RunningMoments:
    """Welford one-pass running mean/variance."""
    n: int = 0
    mean: float = 0.0
    M2: float = 0.0  # sum of squared deviations

    def update(self, x: float):
        self.n += 1
        delta = x - self.mean
        self.mean += delta / self.n
        self.M2 += delta * (x - self.mean)

    @property
    def var_unbiased(self) -> float:
        return self.M2 / (self.n - 1) if self.n >= 2 else np.nan

    @property
    def sd_unbiased(self) -> float:
        v = self.var_unbiased
        return np.sqrt(v) if np.isfinite(v) and v >= 0 else np.nan


@dataclass
class _NormalState:
    mom: _RunningMoments

class NormalPluginPredictive(PredictiveMethod):
    """
    Plug-in Normal predictive: N(mu_hat, sigma_hat^2) from running mean/variance.
    """
    def __init__(self):
        pass

    def init_state(self, **kwargs: Any) -> PredictiveState:
        return _NormalState(mom=_RunningMoments())

    def update(self, state: _NormalState, x: float) -> _NormalState:
        state.mom.update(x)
        return state

    def _params(self, state: _NormalState):
        n = state.mom.n
        mu = state.mom.mean if n >= 1 else 0.0
        sd = state.mom.sd_unbiased if n >= 2 else np.nan  # undefined until n>=2
        return n, mu, sd

    def cdf_est(self, state: _NormalState, tval: Array) -> Array:
        n, mu, sd = self._params(state)
        tval = np.asarray(tval)
        if n < 2 or not np.isfinite(sd) or sd <= 0:
            # fallback: before enough data, use mu only with unit sd
            return norm.cdf((tval - mu) / 1.0)
        return norm.cdf((tval - mu) / sd)

    def pdf_est(self, state: _NormalState, x: Array) -> Array:
        n, mu, sd = self._params(state)
        x = np.asarray(x)
        if n < 2 or not np.isfinite(sd) or sd <= 0:
            return norm.pdf((x - mu) / 1.0) / 1.0
        return norm.pdf((x - mu) / sd) / sd


@dataclass
class _TState:
    mom: _RunningMoments

class StudentTPredictive(PredictiveMethod):
    """
    Conjugate Normal–Inverse-Gamma with (effectively) noninformative prior.
    One-step predictive: t_{n-1}((x - xbar) / (s * sqrt(1 + 1/n))) for n>=2.
    """
    def __init__(self):
        pass

    def init_state(self, **kwargs: Any) -> PredictiveState:
        return _TState(mom=_RunningMoments())

    def update(self, state: _TState, x: float) -> _TState:
        state.mom.update(x)
        return state

    def _t_params(self, state: _TState):
        n = state.mom.n
        xbar = state.mom.mean if n >= 1 else 0.0
        s = state.mom.sd_unbiased  # sample sd (n>=2 to be finite)
        df = max(n - 1, 1)         # avoid df<=0; will guard in cdf/pdf
        scale = s * np.sqrt(1.0 + 1.0 / n) if n >= 1 and np.isfinite(s) else np.nan
        return n, xbar, df, scale

    def cdf_est(self, state: _TState, tval: Array) -> Array:
        n, xbar, df, scale = self._t_params(state)
        tval = np.asarray(tval)
        if n < 2 or not np.isfinite(scale) or scale <= 0:
            # before we have variance info, fall back to standard normal around xbar
            return norm.cdf(tval - xbar)
        z = (tval - xbar) / scale
        return t.cdf(z, df=df)

    def pdf_est(self, state: _TState, x: Array) -> Array:
        n, xbar, df, scale = self._t_params(state)
        x = np.asarray(x)
        if n < 2 or not np.isfinite(scale) or scale <= 0:
            return norm.pdf(x - xbar)
        z = (x - xbar) / scale
        # t.pdf is for standardized t; divide by scale for actual density
        return t.pdf(z, df=df) / scale
