import pathlib, subprocess

def test_partc_pooled_z_pipeline(tmp_path):
    raw = pathlib.Path("results/raw")
    figs = pathlib.Path("results/figures")
    raw.mkdir(parents=True, exist_ok=True)
    figs.mkdir(parents=True, exist_ok=True)

    # tiny run
    subprocess.run(
        "python -m src_cli.partc_log_prop26 --alpha 5 --t 0.5 "
        "--n 100 --M 100 --seed 1 --base uniform",
        shell=True, check=True
    )
    csvs = list(raw.glob("prop26_*_a5.0_*_uniform.csv"))
    assert csvs, "expected prop26 raw CSV"

    # figure
    subprocess.run(
        f"python -m src_cli.partc_figures_prop26 --csv {csvs[0]} --title 'test'",
        shell=True, check=True
    )
    pngs = list(figs.glob("prop26_zcheck_*.png"))
    assert pngs, "expected pooled-Z PNG"
