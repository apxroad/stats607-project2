from __future__ import annotations

from dataclasses import dataclass
from typing import Union, Iterable, overload
import numpy as np
from scipy.special import erf  

ArrayLike = Union[np.ndarray, float]

__all__ = [
    "NormalTruth",
    "UniformTruth",
    "sample_truth",
    "cdf_truth",
    "pdf_truth",
]

# ----------------------------
# Standard Normal helpers
# ----------------------------

def _phi(x: ArrayLike) -> ArrayLike:
    """Standard normal PDF."""
    x = np.asarray(x, dtype=float)
    return np.exp(-0.5 * x**2) / np.sqrt(2.0 * np.pi)

def _Phi(x: ArrayLike) -> ArrayLike:
    """Standard normal CDF."""
    x = np.asarray(x, dtype=float)
    return 0.5 * (1.0 + erf(x / np.sqrt(2.0)))

# ----------------------------
# Truth classes
# ----------------------------

@dataclass
class NormalTruth:
    """
    Oracle truth F for a Normal(mean, sd) distribution.
    Defaults to N(0,1) (the baseline in many experiments).
    """
    mean: float = 0.0
    sd: float = 1.0

    def sample(self, n: int, seed: int | None = None) -> np.ndarray:
        rng = np.random.default_rng(seed)
        z = rng.standard_normal(int(n))
        return self.mean + self.sd * z

    def cdf_truth(self, t: ArrayLike) -> ArrayLike:
        t = np.asarray(t, dtype=float)
        if self.sd == 1.0 and self.mean == 0.0:
            return _Phi(t)
        z = (t - self.mean) / self.sd
        return _Phi(z)

    def pdf_truth(self, x: ArrayLike) -> ArrayLike:
        x = np.asarray(x, dtype=float)
        if self.sd == 1.0 and self.mean == 0.0:
            return _phi(x)
        z = (x - self.mean) / self.sd
        return _phi(z) / self.sd


@dataclass
class UniformTruth:
    """
    Oracle truth F for a Uniform(a, b) distribution.
    Defaults to U(0,1) to match classic DP/Pólya examples.
    """
    a: float = 0.0
    b: float = 1.0

    def sample(self, n: int, seed: int | None = None) -> np.ndarray:
        rng = np.random.default_rng(seed)
        return rng.uniform(self.a, self.b, size=int(n))

    def cdf_truth(self, t: ArrayLike) -> ArrayLike:
        t = np.asarray(t, dtype=float)
        a, b = float(self.a), float(self.b)
        out = (t - a) / (b - a)
        return np.clip(out, 0.0, 1.0)

    def pdf_truth(self, x: ArrayLike) -> ArrayLike:
        x = np.asarray(x, dtype=float)
        a, b = float(self.a), float(self.b)
        inside = (x >= a) & (x <= b)
        val = np.zeros_like(x, dtype=float)
        val[inside] = 1.0 / (b - a)
        # Return scalar if input was scalar
        if np.ndim(x) == 0:
            return float(val)
        return val

# ----------------------------
# Convenience functions (Normal by default)
# ----------------------------

def sample_truth(n: int, seed: int | None = None) -> np.ndarray:
    """
    Backward-compatible helper used in earlier steps.
    Draws from Normal(0,1). For Uniform base, instantiate UniformTruth() directly.
    """
    return NormalTruth().sample(n=n, seed=seed)

def cdf_truth(t: ArrayLike) -> ArrayLike:
    """
    Backward-compatible helper: CDF of Normal(0,1).
    For Uniform base, use UniformTruth().cdf_truth(t).
    """
    return NormalTruth().cdf_truth(t)

def pdf_truth(x: ArrayLike) -> ArrayLike:
    """
    Backward-compatible helper: PDF of Normal(0,1).
    For Uniform base, use UniformTruth().pdf_truth(x).
    """
    return NormalTruth().pdf_truth(x)
