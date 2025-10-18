from __future__ import annotations
import glob, os
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yaml

def plot_convergence(raw_files: list[str], outdir: str):
    # plot d_infty and d_rmse vs i for each method (one example file per method/n)
    examples = {}
    for f in raw_files:
        df = pd.read_parquet(f)
        key = (df["method"].iloc[0], int(df["n"].iloc[0]))
        # keep the first file we see for each (method,n)
        if key not in examples:
            examples[key] = df

    for (method, n), df in examples.items():
        fig1 = plt.figure()
        plt.plot(df["i"], df["d_infty"], label=r"$d^{(\infty)}$")
        plt.xlabel("step i")
        plt.ylabel(r"$d^{(\infty)}$")
        plt.title(f"Convergence: {method}, n={n}")
        plt.legend()
        plt.tight_layout()
        p1 = os.path.join(outdir, f"conv_dinf_{method}_n{n}.png")
        fig1.savefig(p1)
        plt.close(fig1)

        fig2 = plt.figure()
        plt.plot(df["i"], df["d_rmse"], label="RMSE")
        plt.xlabel("step i")
        plt.ylabel("RMSE")
        plt.title(f"Convergence: {method}, n={n}")
        plt.legend()
        plt.tight_layout()
        p2 = os.path.join(outdir, f"conv_rmse_{method}_n{n}.png")
        fig2.savefig(p2)
        plt.close(fig2)

def plot_pit_hist(raw_files: list[str], outdir: str):
    # combine PIT across reps per (method, n)
    frames = []
    for f in raw_files:
        df = pd.read_parquet(f)[["method","n","pit"]].dropna()
        frames.append(df)
    if not frames:
        return
    allpit = pd.concat(frames, ignore_index=True)

    for (method, n), grp in allpit.groupby(["method","n"]):
        fig = plt.figure()
        plt.hist(grp["pit"].values, bins=20, density=True, edgecolor="black")
        plt.xlabel("PIT")
        plt.ylabel("Density")
        plt.title(f"PIT histogram: {method}, n={int(n)}")
        plt.tight_layout()
        p = os.path.join(outdir, f"pit_{method}_n{int(n)}.png")
        fig.savefig(p)
        plt.close(fig)

def main():
    ap = argparse.ArgumentParser(description="Make baseline figures")
    ap.add_argument("--config", required=True)
    args = ap.parse_args()

    cfg = yaml.safe_load(open(args.config, "r"))
    raw_dir = cfg["io"]["raw_dir"]
    fig_dir = cfg["io"]["fig_dir"]
    Path(fig_dir).mkdir(parents=True, exist_ok=True)

    files = sorted(glob.glob(os.path.join(raw_dir, "*.parquet")))
    if not files:
        print("[figures] no raw files found — run simulate first.")
        return

    plot_convergence(files, fig_dir)
    plot_pit_hist(files, fig_dir)
    print("[figures] wrote figures to", fig_dir)

if __name__ == "__main__":
    main()
