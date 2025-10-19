from pathlib import Path
import pandas as pd
from src.simulation import run_stream

def test_reproducible_output(tmp_path: Path):
    out1 = tmp_path / "a.parquet"
    out2 = tmp_path / "b.parquet"

    # tiny Pólya run (Uniform base, to match our config)
    kwargs = dict(
        method_name="polya_dp",
        n=120,
        J=20,
        tmin=0.0,
        tmax=1.0,
        record_every=10,
        seed=123,
        alpha=5.0,
        base="uniform",
    )

    run_stream(out_path=str(out1), **kwargs)
    run_stream(out_path=str(out2), **kwargs)

    df1 = pd.read_parquet(out1)
    df2 = pd.read_parquet(out2)
    # exact equality with fixed RNG + same code path
    assert df1.equals(df2)
