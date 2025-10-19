# Analysis Summary — Setting 1 (DP/Pólya, Uniform base)

**Prior/Posterior Beta laws.**
Histograms of \(F(({-}\infty,t])\) align with \(\mathrm{Beta}(\alpha G_0(t), \alpha (1-G_0(t)))\) (prior)
and \(\mathrm{Beta}(\alpha G_0(t)+K_n, \alpha(1-G_0(t))+n-K_n)\) (posterior).

**Predictive calibration.**
PIT histograms are close to uniform, confirming calibrated sequential predictives under exchangeability.

**Convergence.**
\(d^{(\infty)}\) and RMSE shrink as the stream index \(i\) grows.

**Coverage.**
Equal-tailed 95% Beta intervals achieve \(\approx 0.95\) coverage across \(t\) and \(n\).

**M-sensitivity.**
Bias and coverage curves stabilize with \(M\) (roughly \(1/\sqrt{M}\) MC error).

**Reproduce.** `make everything`  
Figures in `results/figures/`; raw parquet in `results/raw/`.