from __future__ import annotations
import argparse, numpy as np, matplotlib.pyplot as plt
from scipy.stats import beta
from src.dgps import UniformTruth, NormalTruth

def draw_prior_samples(alpha: float, p0: float, reps: int, rng) -> np.ndarray:
    a0, b0 = alpha * p0, alpha * (1.0 - p0)
    return beta.rvs(a0, b0, size=reps, random_state=rng)

def draw_posterior_samples(alpha: float, p0: float, n: int, reps: int, rng) -> np.ndarray:
    draws = np.empty(reps, dtype=float)
    for r in range(reps):
        K = 0
        for i in range(1, n+1):
            p_i = (alpha * p0 + K) / (alpha + i - 1)
            K += rng.random() < p_i
        a_post = alpha * p0 + K
        b_post = alpha * (1.0 - p0) + (n - K)
        draws[r] = beta.rvs(a_post, b_post, random_state=rng)
    return draws

def main():
    ap = argparse.ArgumentParser(description="Panels of prior/posterior Beta overlays across t and alpha")
    ap.add_argument("--base", type=str, default="uniform", choices=["uniform","normal"])
    ap.add_argument("--ts", nargs="+", type=float, default=[0.25, 0.5, 0.75], help="thresholds t")
    ap.add_argument("--alphas", nargs="+", type=float, default=[1.0, 5.0, 20.0], help="alpha grid")
    ap.add_argument("--n", type=int, default=100, help="n for posterior experiment")
    ap.add_argument("--reps", type=int, default=4000, help="MC repetitions")
    ap.add_argument("--seed", type=int, default=20251018)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    G0  = UniformTruth(0.0, 1.0) if args.base == "uniform" else NormalTruth()

    ts = np.array(args.ts, dtype=float)
    alphas = np.array(args.alphas, dtype=float)

    # PRIOR panel
    fig_prior, axes_prior = plt.subplots(len(ts), len(alphas), figsize=(4*len(alphas), 3*len(ts)), squeeze=False)
    x = np.linspace(0, 1, 400)
    for i, t in enumerate(ts):
        p0 = float(G0.cdf_truth(t))
        for j, a in enumerate(alphas):
            ax = axes_prior[i, j]
            samples = draw_prior_samples(a, p0, args.reps, rng)
            a0, b0 = a * p0, a * (1.0 - p0)
            ax.hist(samples, bins=40, density=True, alpha=0.5, edgecolor="black")
            ax.plot(x, beta.pdf(x, a0, b0), lw=2)
            ax.axvline(p0, ls="--")
            ax.set_title(f"Prior | t={t:.2f}, α={a:g}")
            ax.set_xlim(0,1)
            if i == len(ts)-1: ax.set_xlabel("P((−∞, t])")
            if j == 0: ax.set_ylabel("Density")
    fig_prior.tight_layout()
    fig_prior.savefig("results/figures/polya_prior_panels.png", dpi=150)
    plt.close(fig_prior)

    # POSTERIOR panel
    fig_post, axes_post = plt.subplots(len(ts), len(alphas), figsize=(4*len(alphas), 3*len(ts)), squeeze=False)
    for i, t in enumerate(ts):
        p0 = float(G0.cdf_truth(t))
        for j, a in enumerate(alphas):
            ax = axes_post[i, j]
            samples = draw_posterior_samples(a, p0, args.n, args.reps, rng)
            # reference Beta using average K for a smooth overlay
            Ks = []
            for _ in range(200):
                K = 0
                for ii in range(1, args.n+1):
                    p_i = (a * p0 + K) / (a + ii - 1)
                    K += rng.random() < p_i
                Ks.append(K)
            Kbar = float(np.mean(Ks))
            a_bar = a * p0 + Kbar
            b_bar = a * (1.0 - p0) + (args.n - Kbar)

            ax.hist(samples, bins=40, density=True, alpha=0.5, edgecolor="black")
            ax.plot(x, beta.pdf(x, a_bar, b_bar), lw=2)
            ax.axvline(p0, ls="--")
            ax.set_title(f"Posterior | t={t:.2f}, α={a:g}, n={args.n}")
            ax.set_xlim(0,1)
            if i == len(ts)-1: ax.set_xlabel("P((−∞, t])")
            if j == 0: ax.set_ylabel("Density")
    fig_post.tight_layout()
    fig_post.savefig("results/figures/polya_posterior_panels.png", dpi=150)
    plt.close(fig_post)

    print("Wrote figures: results/figures/polya_prior_panels.png and polya_posterior_panels.png")

if __name__ == "__main__":
    main()
