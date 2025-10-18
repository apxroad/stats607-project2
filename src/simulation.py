from __future__ import annotations
import os
from pathlib import Path
import numpy as np
import pandas as pd

from .dgps import NormalTruth         # baseline truth
from .metrics import d_infty, d_rmse, make_grid
from .methods import EmpiricalPredictive, NormalPluginPredictive, StudentTPredictive

# map names in config -> classes
METHODS = {
    "empirical_ecdf": EmpiricalPredictive,
    "normal_plugin": NormalPluginPredictive,
    "student_t_conjugate": StudentTPredictive,
}

def _build_method(method_name: str, n: int):
    if method_name == "empirical_ecdf":
        return EmpiricalPredictive(max_n=n), "empirical_ecdf"
    elif method_name == "normal_plugin":
        return NormalPluginPredictive(), "normal_plugin"
    elif method_name == "student_t_conjugate":
        return StudentTPredictive(), "student_t_conjugate"
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
) -> str:
    """
    Stream X_1..X_n ~ N(0,1). Before seeing X_i, evaluate predictive CDF on grid,
    compute distances to oracle, record PIT; then update with X_i. Save parquet.
    """
    rng = np.random.default_rng(seed)
    truth = NormalTruth()
    x = truth.sample(n=n, seed=seed)

    t_grid = make_grid(J, tmin, tmax)
    c_true_grid = truth.cdf_truth(t_grid)

    method, mname = _build_method(method_name, n)
    # init_state: ECDF needs max_n, others ignore kwargs
    try:
        state = method.init_state(max_n=n)  # works for ECDF
    except TypeError:
        state = method.init_state()

    recs = []
    for i in range(n):
        x_i = x[i]

        # evaluate BEFORE observing x_i
        # PIT requires cdf_est at x_i before update
        if i == 0:
            pit_i = np.nan
            d_inf_i = np.nan
            d_rmse_i = np.nan
        else:
            # pit
            pit_i = float(method.cdf_est(state, x_i))
            # distances on grid (thinned)
            if (i % record_every) == 0 or i == n - 1:
                c_est_grid = np.asarray(method.cdf_est(state, t_grid), dtype=float)
                d_inf_i = d_infty(c_est_grid, c_true_grid)
                d_rmse_i = d_rmse(c_est_grid, c_true_grid)
            else:
                d_inf_i = np.nan
                d_rmse_i = np.nan

        recs.append((i, mname, x_i, pit_i, d_inf_i, d_rmse_i, seed, n))

        # now update with x_i
        state = method.update(state, float(x_i))

    df = pd.DataFrame(
        recs, columns=["i", "method", "x_i", "pit", "d_infty", "d_rmse", "seed", "n"]
    )

    Path(os.path.dirname(out_path)).mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)
    return out_path
