# ADEMP — Pólya/DP Baseline
**Aims.** Verify DP/Pólya one-step predictive against theory under Uniform(0,1) base:
- Prior/posterior Beta at single t; 
- Across-rep mean/var match; 95% CI coverage.

**Data.** X₁:n ~ G₀, with G₀ = Uniform(0,1). n ∈ {100,500,1000}. M = reps per n.

**Estimand/Estimates.** For each t ∈ {0.25,0.5,0.75}, target F₀(t)=G₀(t).
Estimate with Pólya predictive: \tilde Pₙ((−∞,t]) = (αG₀(t)+Kₙ(t))/(α+n).

**Methods.** Dirichlet-process (α∈{1,5,20}), base = Uniform. Metrics: PIT, d^(∞), RMSE.
Summaries: empirical mean/var across reps vs theory; Beta CI coverage.

**Performance.**
- Expect emp_mean ≈ theory_mean (=G₀(t))
- emp_var ≈ n·G₀(t)[1−G₀(t)]/(α+n)²
- coverage ≈ 0.95 (Beta posterior CI).
