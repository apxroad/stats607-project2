# ANALYSIS — What the figures show and how to read them

This document links each figure to the DP/Pólya theory (Section 2.4) and states the expected pattern.

---

## 1) Prior & Posterior panels (Part A)
- **What**: For each (t, α) we draw Monte‑Carlo samples of F((−∞,t]) using the *continuation* mechanism
  (prior: n=0; posterior: fix x₁:ₙ and continue). We overlay the **exact Beta** density:
  - Prior: Beta(α t, α(1−t)).
  - Posterior: Beta(α t + kₙ, α(1−t) + n − kₙ).
- **Expect**: Histogram lines up with the orange Beta curve; spread shrinks as α increases (prior) and as n increases (posterior).

## 2) Predictive learning diagnostics (Part B)
- **PIT histogram**: Uᵢ = P_{i−1}(Xᵢ) should be ~ Uniform(0,1); flat bars indicate calibrated exchangeable predictives.
- **Convergence curves**: distances between the predictive CDF and the ground truth baseline decrease with i (stabilization).
- **Predictive paths**: lines m↦Pₘ(t) flatten as m grows and hover around t when G₀ is Uniform(0,1).

## 3) Proposition 2.6 confidence intervals (Part C)
- **Object**: a **predictive-only** CI for the *limit mass* F̃(t).
- **Construction**: Pₙ(t) ± z_{.975} √(Vₙ,t / n), Vₙ,t = (1/n)∑ m²(Pₘ−P_{m−1})² from the *same* predictive path.
- **Target for evaluation**: F̂(t) obtained by continuing the same urn far into the tail and averaging 1{X≤t}.
- **Expect**: coverage near nominal and improving with n; mean width decreases with n; pooled Z = (Pₙ−F̂)/√(Vₙ/n) looks ~Normal.

---

## Reading tips
- Dashed **y=t** lines in path figures are the Uniform(0,1) baseline under G₀=Uniform.
- Where present, dashed **0.95** lines mark nominal coverage.
- Figures named `*_vs_M` show Monte‑Carlo stability: bias and coverage flatten at ≈1/√M.
