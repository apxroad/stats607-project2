import argparse
from pathlib import Path
import os, pandas as pd

def main():
    ap = argparse.ArgumentParser(description="Summarize raw outputs into tidy CSVs.")
    ap.add_argument("--raw", default="results/raw", help="raw results dir")
    ap.add_argument("--summary", default="results/summary", help="summary output dir")
    ap.add_argument("--alpha", type=float, default=5.0)
    ap.add_argument("--seed", type=int, default=2025)
    ap.add_argument("--base", choices=["uniform","normal"], default="uniform")
    ap.add_argument("--stem", default="partB_n1000_a5.0_seed2025_uniform")
    args = ap.parse_args()

    raw = Path(args.raw); raw.mkdir(parents=True, exist_ok=True)
    out = Path(args.summary); out.mkdir(parents=True, exist_ok=True)

    # ---- Prop 2.6 summary (coverage/width by n,t)
    prop26 = raw / f"prop26_M400_L50000_a{args.alpha}_seed{args.seed}_{args.base}.csv"
    if prop26.exists():
        df = pd.read_csv(prop26)
        summ = (df.groupby(["n","t"])
                  .agg(coverage=("covered","mean"),
                       mean_width=("width","mean"),
                       reps=("rep","nunique"))
                  .reset_index())
        summ.to_csv(out / "prop26_summary.csv", index=False)
        print(f"[ok] wrote {out/'prop26_summary.csv'}")
    else:
        print(f"[skip] missing {prop26}")

    # ---- Part B distances quick summary
    dfile = raw / f"distances_{args.stem}.csv"
    if dfile.exists():
        d  = pd.read_csv(dfile)
        sm = d.agg({"d_infty":["mean","min","max"], "d_rmse":["mean","min","max"]})
        (out / "partB_distances_summary.csv").write_text(sm.to_csv())
        print(f"[ok] wrote {out/'partB_distances_summary.csv'}")
    else:
        print(f"[skip] missing {dfile}")

if __name__ == "__main__":
    main()
