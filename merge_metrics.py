
import pandas as pd
from pathlib import Path

metrics_files = list(Path("outputs").glob("metrics_*.csv"))

dfs = []
for f in metrics_files:
    df = pd.read_csv(f)
    dfs.append(df)

all_metrics = pd.concat(dfs, ignore_index=True)
all_metrics.to_csv("outputs/all_metrics.csv", index=False, encoding="utf-8-sig")

print(all_metrics)