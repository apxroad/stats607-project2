import argparse, os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

from src.polya import PolyaSequenceModel

def run_once(n:int, alpha:float, ts, seed:int, base:str):
    rng = np.random.default_rng(seed)
    model = PolyaSequenceModel(alpha=alpha, base=base)

    xs = []
    x0 = (rng.random() if base=="uniform" else rng.standard_normal())
    xs.append(x0)
    for m in range(1, n):
        xs.append(model.Pn(m, xs))

    # running counts K_m(t) = #{i<=m : x_i <= t}
    xs_arr = np.asarray(xs)
    rows = []
    for m in range(1, n+1):
        Km = {}
        for t in ts:
            Km[t] = int(np.sum(xs_arr[:m] <= t))
        for t in ts:
            Pm = (alpha*t + Km[t])/(alpha + m)   # predictive CDF at t before seeing x_{m+1}
            rows.append((m, float(t), float(Pm)))
    df = pd.DataFrame(rows, columns=["m","t","Pm"])
    return xs_arr, df

def main():
    ap = argparse.ArgumentParser(description="Log predictive CDF path m↦Pm(t) for chosen t's (one stream).")
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--alpha", type=float, default=5.0)
    ap.add_argument("--t", type=float, nargs="+", default=[0.25,0.5,0.75])
    ap.add_argument("--seed", type=int, default=2025)
    ap.add_argument("--base", choices=["uniform","normal"], default="uniform")
    args = ap.parse_args()

    _, df = run_once(args.n, args.alpha, args.t, args.seed, args.base)

    outdir = Path("results/raw"); outdir.mkdir(parents=True, exist_ok=True)
    tag = f"n{args.n}_a{args.alpha}_seed{args.seed}_{args.base}"
    csv_path = outdir / f"predictive_path_{tag}.csv"
    df.to_csv(csv_path, index=False)
    print(f"[ok] wrote {csv_path}")

if __name__ == "__main__":
    main()
