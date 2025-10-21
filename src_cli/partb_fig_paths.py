import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def main():
    ap = argparse.ArgumentParser(description="Plot predictive paths m↦Pm(t) from a CSV produced by log_predictive_paths.py")
    ap.add_argument("--csv", type=str, required=True)
    ap.add_argument("--title", type=str, default="Predictive paths m ↦ Pm(t)")
    args = ap.parse_args()

    df = pd.read_csv(args.csv)
    ts = sorted(df["t"].unique())
    fig, axes = plt.subplots(len(ts), 1, figsize=(7, 2.6*len(ts)), sharex=True)
    if len(ts)==1: axes=[axes]

    for ax, t in zip(axes, ts):
        sub = df[df["t"]==t].sort_values("m")
        ax.plot(sub["m"], sub["Pm"], lw=1.6)
        ax.axhline(t, ls="--", color="k", lw=1)  # baseline for Unif(0,1)
        ax.set_ylabel(f"P_m({t})")
        ax.set_ylim(0,1)
        ax.grid(alpha=.25, linestyle=":", linewidth=.8)

    axes[-1].set_xlabel("m (step)")
    fig.suptitle(args.title)
    fig.tight_layout(rect=[0,0,1,0.95])

    outdir = Path("results/figures"); outdir.mkdir(parents=True, exist_ok=True)
    stem = Path(args.csv).stem.replace("predictive_path_", "predictive_paths_")
    png = outdir / f"{stem}.png"
    fig.savefig(png, dpi=140)
    plt.close(fig)
    print(f"[ok] wrote {png}")

if __name__ == "__main__":
    main()
