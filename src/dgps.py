from __future__ import annotations
import numpy as np
from dataclasses import dataclass
from math import erf, sqrt
from typing import Union
from .interfaces import Truth

ArrayLike = Union[np.ndarray, float]

def _phi(x: ArrayLike) -> ArrayLike:
    x = np.asarray(x)
    return np.exp(-0.5 * x**2) / np.sqrt(2.0 * np.pi)

def _Phi(x: ArrayLike) -> ArrayLike:
    x = np.asarray(x)
    return 0.5 * (1.0 + erf(x / sqrt(2.0)))

@dataclass
class NormalTruth(Truth):
    mean: float = 0.0
    sd: float = 1.0

    def sample(self, n: int, seed: int | None = None) -> np.ndarray:
        rng = np.random.default_rng(seed)
        z = rng.standard_normal(n)
        return self.mean + self.sd * z

    def cdf_truth(self, t: ArrayLike) -> ArrayLike:
        if self.mean == 0.0 and self.sd == 1.0:
            return _Phi(t)
        z = (np.asarray(t) - self.mean) / self.sd
        return _Phi(z)

    def pdf_truth(self, x: ArrayLike) -> ArrayLike:
        if self.mean == 0.0 and self.sd == 1.0:
            return _phi(x)
        z = (np.asarray(x) - self.mean) / self.sd
        return _phi(z) / self.sd

# Convenience functions matching config "truth: Normal(0,1)"
def sample_truth(n: int, seed: int | None = None) -> np.ndarray:
    return NormalTruth().sample(n=n, seed=seed)

def cdf_truth(t: ArrayLike) -> ArrayLike:
    return NormalTruth().cdf_truth(t)

def pdf_truth(x: ArrayLike) -> ArrayLike:
    return NormalTruth().pdf_truth(x)
