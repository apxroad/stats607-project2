# ADEMP — Baseline (i.i.d. Normal)

## Aims (A)
Assess one-step calibration and convergence of predictive CDFs under i.i.d. \(\mathcal N(0,1)\); compare ECDF vs Normal-based predictives.

## Data-Generating Mechanisms (D)
- Truth \(F\): \(\mathcal N(0,1)\).
- Stream lengths \(n \in \{1000, 5000\}\).
- Repetitions: 10 (initial; scalable).
- Grid: \(J=100\) points on \([-4,4]\).

## Estimands (E)
- Predictive CDF on grid \(\{t_j\}\).
- Quantiles \(q_{0.1}, q_{0.5}, q_{0.9}\).
- PIT values \(U_i=\tilde P_{i-1}(X_i)\).

## Methods (M)
- Empirical ECDF (baseline).
- Normal plug-in predictive (online \(\hat\mu_n,\hat\sigma_n\)).
- Conjugate \(t\)-predictive (Normal–Inverse-Gamma).

## Performance Measures (P)
- Distances to oracle \(F\): \(d^{(\infty)}\) and RMSE over the grid.
- PIT histograms; simple uniformity summary.
- (Later) mean log predictive density once \(pdf\) is exposed.

### Design Table
| Factor  | Levels                                  |
|-------: |:----------------------------------------|
| Truth   | \(\mathcal N(0,1)\)                     |
| \(n\)   | 1000, 5000                              |
| Reps    | 10                                      |
| Grid    | \(J=100\) on \([-4,4]\)                 |
| Methods | ECDF, Normal plug-in, Conjugate \(t\)   |
| Metrics | PIT, \(d^{(\infty)}\), RMSE (every 50)  |
