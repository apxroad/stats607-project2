from pathlib import Path
import pandas as pd, subprocess, sys

def test_partb_smoke(tmp_path: Path):
    # very small run
    cmd = [sys.executable, "-m", "src_cli.partb_log_convergence",
           "--n", "50", "--alpha", "5", "--t", "0.5", "--seed", "123", "--base", "uniform"]
    subprocess.run(cmd, check=True)

    raw = Path("results/raw")
    dfs = list(raw.glob("distances_partB_n50_a5.0_seed123_uniform.csv")) +           list(raw.glob("Pm_paths_partB_n50_a5.0_seed123_uniform.csv"))
    assert dfs, "Expected small CSVs in results/raw"

    d = pd.read_csv(raw / "distances_partB_n50_a5.0_seed123_uniform.csv")
    assert {"i","d_infty","d_rmse"} <= set(d.columns)
