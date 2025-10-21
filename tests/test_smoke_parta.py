import pathlib, subprocess, sys

def test_parta_prior_runs(tmp_path):
    out = tmp_path / "figures"
    out.mkdir(parents=True, exist_ok=True)
    # run with tiny M,N to keep fast
    cmd = (
        "python -m src_cli.parta_panels "
        "--base uniform --t 0.5 --alpha 5 --n 0 --M 50 --N 50 --seed 1"
    )
    subprocess.run(cmd, shell=True, check=True)
    # confirm at least one panel exists
    figs = list(pathlib.Path("results/figures").glob("post_panels_cont_n0_*.png"))
    assert figs, "expected a prior panel PNG to be written"
