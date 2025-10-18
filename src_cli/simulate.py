from __future__ import annotations
import os
import argparse
from pathlib import Path
import yaml

from src.simulation import run_stream

def main():
    ap = argparse.ArgumentParser(description="Run baseline simulation(s)")
    ap.add_argument("--config", required=True, help="Path to YAML config")
    args = ap.parse_args()

    cfg = yaml.safe_load(open(args.config, "r"))
    n_list      = cfg["n"]
    reps        = int(cfg["reps"])
    J           = int(cfg["grid"]["J"])
    tmin        = float(cfg["grid"]["tmin"])
    tmax        = float(cfg["grid"]["tmax"])
    methods     = list(cfg["methods"])
    record_every= int(cfg["metrics"]["record_every"])
    raw_dir     = cfg["io"]["raw_dir"]
    base_seed   = int(cfg["seeding"]["base"])

    Path(raw_dir).mkdir(parents=True, exist_ok=True)

    for method in methods:
        for n in n_list:
            for rep in range(reps):
                seed = base_seed + 1000 * int(n) + int(rep)  # deterministic per cell
                out = os.path.join(raw_dir, f"{method}_n{n}_rep{rep}.parquet")
                print(f"[simulate] method={method} n={n} rep={rep} seed={seed} -> {out}")
                run_stream(
                    method_name=method,
                    n=int(n),
                    J=J,
                    tmin=tmin,
                    tmax=tmax,
                    record_every=record_every,
                    seed=seed,
                    out_path=out,
                )

if __name__ == "__main__":
    main()
