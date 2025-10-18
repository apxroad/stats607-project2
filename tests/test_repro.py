from pathlib import Path
import pandas as pd
from src.simulation import run_stream

def test_reproducible_output(tmp_path: Path):
    out1 = tmp_path / "a.parquet"
    out2 = tmp_path / "b.parquet"
    # tiny run
    run_stream(method_name="empirical_ecdf", n=120, J=20, tmin=-3, tmax=3,
               record_every=10, seed=123, out_path=str(out1))
    run_stream(method_name="empirical_ecdf", n=120, J=20, tmin=-3, tmax=3,
               record_every=10, seed=123, out_path=str(out2))
    df1 = pd.read_parquet(out1)
    df2 = pd.read_parquet(out2)
    # exact equality is OK because we use fixed RNG + same code path
    assert df1.equals(df2)
