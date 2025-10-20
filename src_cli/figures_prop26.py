import argparse
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.plotstyle import use_nice_style

def main():
    use_nice_style()
    ap = argparse.ArgumentParser(description="Figures for Prop 2.6: coverage vs n and CI width vs n.")
    ap.add_argument("--csv", required=True, help="results/raw/prop26_*.csv produced by log_prop26.py")
    ap.add_argument("--title", default="", help="figure title suffix")
    args = ap.parse_args()

    raw = Path(args.csv)
    if not raw.exists():
        raise FileNotFoundError(raw)

    df = pd.read_csv(raw)

    outdir = Path("results/figures"); outdir.mkdir(parents=True, exist_ok=True)
    base = df["base"].iloc[0]; alpha = df["alpha"].iloc[0]

    # ---------- coverage vs n (faceted by t) ----------
    tvals = sorted(df["t"].unique())
    fig, axes = plt.subplots(len(tvals), 1, figsize=(6.6, 3.1*len(tvals)), sharex=True)
    if len(tvals) == 1: axes = [axes]

    for ax, t in zip(axes, tvals):
        sub = df[df["t"] == t]
        gg = (sub.groupby("n", as_index=False)
                 .agg(coverage=("covered","mean")))
        ax.plot(gg["n"], gg["coverage"], marker="o")
        ax.axhline(0.95, ls="--", color="k", lw=1)
        ax.set_ylim(0.7, 1.0)
        ax.set_title(f"Coverage vs n (t={t})")
        ax.set_ylabel("Coverage")

    axes[-1].set_xlabel("n")
    ttl = f"Prop 2.6 coverage — base={base}, α={alpha}"
    if args.title: ttl += f" — {args.title}"
    fig.suptitle(ttl, y=0.995, fontsize=12)
    fig.tight_layout()
    out1 = outdir / f"prop26_coverage_{raw.stem.replace('.csv','')}.png"
    fig.savefig(out1, dpi=150); plt.close(fig)
    print(f"[ok] wrote {out1}")

    # ---------- mean CI width vs n (faceted by t) ----------
    fig2, axes2 = plt.subplots(len(tvals), 1, figsize=(6.6, 3.1*len(tvals)), sharex=True)
    if len(tvals) == 1: axes2 = [axes2]

    for ax, t in zip(axes2, tvals):
        sub = df[df["t"] == t]
        gg = (sub.groupby("n", as_index=False)
                 .agg(mean_width=("width","mean")))
        ax.plot(gg["n"], gg["mean_width"], marker="o")
        ax.set_title(f"Mean CI width vs n (t={t})")
        ax.set_ylabel("Mean width")

    axes2[-1].set_xlabel("n")
    ttl = f"Prop 2.6 width — base={base}, α={alpha}"
    if args.title: ttl += f" — {args.title}"
    fig2.suptitle(ttl, y=0.995, fontsize=12)
    fig2.tight_layout()
    out2 = outdir / f"prop26_width_{raw.stem.replace('.csv','')}.png"
    fig2.savefig(out2, dpi=150); plt.close(fig2)
    print(f"[ok] wrote {out2}")

    # ---------- normality check (pooled Z) ----------
    if {"Pn","Fhat","Vnt","n"}.issubset(df.columns):
        z = (df["Pn"] - df["Fhat"]) / np.sqrt(np.maximum(df["Vnt"], 1e-12) / df["n"])
        plt.figure(figsize=(6.2, 4.2))
        plt.hist(z, bins=40, density=True, alpha=0.8)
        plt.title("Prop 2.6 pooled Z = (Pn - Fhat) / sqrt(Vn/n)")
        plt.xlabel("Z"); plt.ylabel("Density")
        out3 = outdir / f"prop26_zcheck_{raw.stem.replace('.csv','')}.png"
        plt.tight_layout()
        plt.savefig(out3, dpi=150); plt.close()
        print(f"[ok] wrote {out3}")

if __name__ == "__main__":
    main()
