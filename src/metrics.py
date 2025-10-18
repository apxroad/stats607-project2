from __future__ import annotations
import numpy as np
from typing import Tuple

def d_infty(c_est: np.ndarray, c_true: np.ndarray) -> float:
    """Sup norm on the grid."""
    return float(np.max(np.abs(c_est - c_true)))

def d_rmse(c_est: np.ndarray, c_true: np.ndarray) -> float:
    """Root-mean-square error on the grid."""
    return float(np.sqrt(np.mean((c_est - c_true) ** 2)))

def make_grid(J: int, tmin: float, tmax: float) -> np.ndarray:
    return np.linspace(float(tmin), float(tmax), int(J))
