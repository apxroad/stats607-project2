from __future__ import annotations
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.plotstyle import apply_plot_style

def normal_pdf(x: np.ndarray) -> np.ndarray:
    return np.exp(-0.5 * x**2) / np.sqrt(2*np.pi)

def extract_Z(df: pd.DataFrame) -> np.ndarray:
    cols = set(df.columns)
    # If 'Z' already exists (older logs), use it.
    if "Z" in cols:
        return df["Z"].to_numpy(dtype=float)
    # Do NOT use lowercase 'z' — that is the CI critical value (≈1.96), not the statistic.
    need = {"Pn", "Fhat", "Vnt", "n"}
    if need.issubset(cols):
        Pn   = df["Pn"].to_numpy(float)
        Fhat = df["Fhat"].to_numpy(float)
        Vnt  = df["Vnt"].to_numpy(float)
        n    = df["n"].to_numpy(float)
        return (Pn - Fhat) / np.sqrt(Vnt / n)
    raise ValueError(f"CSV must contain 'Z' or computable fields {need}. Got: {sorted(cols)}")

def main():
    ap = argparse.ArgumentParser(
        description="Part C — pooled Z only, with N(0,1) overlay (computed from Pn,Fhat,Vnt,n)",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    ap.add_argument("--csv", required=True, help="CSV from partc_log_prop26.py")
    ap.add_argument("--title", default="", help="Custom title (optional)")
    ap.add_argument("--bins", type=int, default=50, help="Histogram bins")
    args = ap.parse_args()

    apply_plot_style()

    df = pd.read_csv(args.csv)
    Z = extract_Z(df)

    # Title bits from CSV (if present)
    alpha = df.get("alpha", pd.Series([None])).iloc[0]
    base  = df.get("base",  pd.Series([None])).iloc[0]
    title_prefix = args.title or f"Proposition 2.6: α={alpha}, base={base}"

    z_mean = float(np.mean(Z))
    z_sd   = float(np.std(Z, ddof=1)) if len(Z) > 1 else 0.0

    # X-range for overlay
    lo, hi = np.min(Z), np.max(Z)
    pad = max(1.5, 3.0*z_sd)
    xs = np.linspace(lo - pad, hi + pad, 1200)

    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    ax.hist(Z, bins=args.bins, density=True, alpha=0.65, edgecolor="none")
    ax.plot(xs, normal_pdf(xs), linewidth=2.0, label="N(0,1) pdf")

    ax.set_xlabel("Z")
    ax.set_ylabel("Density")
    ax.grid(alpha=0.25, linestyle=":", linewidth=0.8)
    ax.legend(frameon=False, loc="upper right")
    fig.suptitle(f"{title_prefix}: pooled Z — mean={z_mean:.2f}, sd={z_sd:.2f}")

    outdir = Path("results/figures"); outdir.mkdir(parents=True, exist_ok=True)
    stem = f"prop26_zcheck_{Path(args.csv).stem}"
    out_png = outdir / f"{stem}.png"
    out_pdf = outdir / f"{stem}.pdf"

    fig.savefig(out_png, dpi=150, bbox_inches="tight")
    fig.savefig(out_pdf, bbox_inches="tight")
    plt.close(fig)

    print(f"[ok] wrote {out_png}")
    print(f"[ok] wrote {out_pdf}")

if __name__ == "__main__":
    main()
