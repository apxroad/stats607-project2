# src/simulation.py
from __future__ import annotations

import os
from pathlib import Path
import numpy as np
import pandas as pd

from .dgps import NormalTruth, UniformTruth
from .metrics import d_infty, d_rmse, make_grid


def _build_method(method_name: str, n: int, **params):
    if method_name == "polya_dp":
        from .methods import PolyaPredictive
        return PolyaPredictive(**params), "polya_dp"
    else:
        raise ValueError(f"Unknown method: {method_name}")


def run_stream(
    method_name: str,
    n: int,
    J: int,
    tmin: float,
    tmax: float,
    record_every: int,
    seed: int,
    out_path: str,
    **params,
) -> str:
    """
    Stream X_1..X_n i.i.d. from the chosen base G0 (Uniform or Normal).
    Before seeing X_i, evaluate the predictive CDF on the grid, record PIT,
    and (thinned) distances to the oracle; then update with X_i. Save parquet.
    """
    rng = np.random.default_rng(seed)

    # pick the truth to match the method's base (exchangeable setup)
    base_name = params.get("base", "uniform")
    if base_name == "uniform":
        truth = UniformTruth(0.0, 1.0)
    else:
        truth = NormalTruth()

    x = truth.sample(n=n, seed=seed)

    # grid and oracle CDF on the grid
    t_grid = make_grid(J, tmin, tmax)
    c_true_grid = truth.cdf_truth(t_grid)

    # build method (Pólya DP) and init its state
    method, mname = _build_method(method_name, n, **params)
    try:
        state = method.init_state(max_n=n)  # some methods may accept this kwarg
    except TypeError:
        state = method.init_state()

    recs = []
    for i in range(n):
        x_i = x[i]

        # Evaluate BEFORE observing x_i (one-step predictive)
        if i == 0:
            pit_i = np.nan
            d_inf_i = np.nan
            d_rmse_i = np.nan
        else:
            # PIT at the realized x_i
            pit_i = float(method.cdf_est(state, x_i))

            # Distances on grid, only at thinned steps or final step
            if (i % record_every) == 0 or i == n - 1:
                c_est_grid = np.asarray(method.cdf_est(state, t_grid), dtype=float)
                d_inf_i = d_infty(c_est_grid, c_true_grid)
                d_rmse_i = d_rmse(c_est_grid, c_true_grid)
            else:
                d_inf_i = np.nan
                d_rmse_i = np.nan

        recs.append((i, mname, x_i, pit_i, d_inf_i, d_rmse_i, seed, n))

        # Update with the new observation
        state = method.update(state, float(x_i))

    df = pd.DataFrame(
        recs,
        columns=["i", "method", "x_i", "pit", "d_infty", "d_rmse", "seed", "n"],
    )

    Path(os.path.dirname(out_path)).mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)
    return out_path
