# ADEMP — Setting 1 (DP/Pólya, Uniform base)

## Aims
Validate exchangeable predictive theory under a Dirichlet Process (DP) prior:
1) Prior/posterior Beta laws for \(F(({-}\infty,t])\);
2) Predictive calibration (PIT \(\sim\) U(0,1));
3) Convergence of predictive CDF to truth;
4) 95% equal-tailed coverage;
5) Monte Carlo stability vs \(M\).

## Data-generating mechanisms (D)
- Base \(G_0 = \mathrm{Unif}(0,1)\).
- \(F \sim \mathrm{DP}(\alpha, G_0)\), \(\alpha \in \{1,5,20\}\).
- Sample sizes \(n \in \{100, 500, 1000\}\).
- Thresholds \(t \in \{0.25, 0.5, 0.75\}\).

## Estimands (E)
- \(F(({-}\infty,t])\) at selected \(t\).
- Predictive CDF \(F_i\) vs truth on a fixed grid; PIT \(U_i = F_i(X_i)\).

## Methods (M)
- Blackwell–MacQueen Pólya predictive:
  \[
  X_{i}\mid X_{1:i-1}\ \sim\ \frac{\alpha}{\alpha+i-1}G_0 + \frac{1}{\alpha+i-1}\sum_{j=1}^{i-1}\delta_{X_j}.
  \]

## Performance (P)
- PIT histogram flatness; distances \(d^{(\infty)}\), RMSE vs step \(i\).
- Beta moments match: empirical mean/variance vs theory.
- 95% equal-tailed posterior CI coverage near 0.95.
- Sensitivity of bias/coverage vs \(M\) (e.g., 30–200).
