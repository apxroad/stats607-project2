from __future__ import annotations
from pathlib import Path
import argparse, numpy as np
import matplotlib.pyplot as plt
from src.plotstyle import apply_plot_style
from scipy.stats import beta
from src.polya import PolyaSequenceModel, build_prefix, continue_urn_once

def panel_for_n(n: int, ts: list[float], alphas: list[float], M: int, N: int, base: str, seed: int):
    rng = np.random.default_rng(seed)
    model = PolyaSequenceModel(alpha=alphas[0], base=base, rng=rng)  # alpha will be reassigned below
    x_obs = build_prefix(n, model)

    fig, axes = plt.subplots(len(ts), len(alphas), figsize=(12, 8), sharex=True, sharey=False)
    axes = np.atleast_2d(axes)

    for i, t in enumerate(ts):
        k_n = sum(1 for x in x_obs if x <= t)
        for j, a in enumerate(alphas):
            model.alpha = a
            post = np.empty(N, dtype=float)
            for r in range(N):
                traj = continue_urn_once(x_obs, model, M)
                post[r] = np.mean(np.asarray(traj) <= t)
            ax = axes[i, j]
            x = np.linspace(0,1,600)
            a_post, b_post = a*t + k_n, a*(1-t) + (n - k_n)
            ax.hist(post, bins=60, density=True, alpha=0.55, edgecolor="black")
            ax.plot(x, beta.pdf(x, a_post, b_post), lw=2.0, color="tab:orange")
            ax.axvline(t, ls="--", lw=1.0, color="tab:blue")
            ax.set_title(f"t={t}, α={a}")
            if j == 0:
                ax.set_ylabel("Density")
            if i == len(ts)-1:
                ax.set_xlabel("P((−∞, t])")

    fig.suptitle(f"Pólya posterior panels  (base={base}, n={n}, M={M}, N={N})")
    fig.tight_layout(rect=[0,0,1,0.96])
    out = f"results/figures/post_panels_cont_n{n}_M{M}_N{N}_{base}.png"
    fig.savefig(out, dpi=140)
    fig.savefig(Path(out).with_suffix('.pdf'))
    plt.close(fig)
    print(f"[ok] wrote {out}")

def main():
    ap = argparse.ArgumentParser(description="Panels of posterior via Pólya continuation.")
    ap.add_argument("--base", choices=["uniform","normal"], default="uniform")
    ap.add_argument("--t", dest="ts", type=float, nargs="+", default=[0.25,0.5,0.75])
    ap.add_argument("--alpha", dest="alphas", type=float, nargs="+", default=[1,5,20])
    ap.add_argument("--n", type=int, default=150)
    ap.add_argument("--M", type=int, default=1000)
    ap.add_argument("--N", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=20250101)
    args = ap.parse_args()
    apply_plot_style()

    panel_for_n(args.n, args.ts, args.alphas, args.M, args.N, args.base, args.seed)

if __name__ == "__main__":
    main()
