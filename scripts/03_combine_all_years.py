from pathlib import Path

import polars as pl

# Directories
ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "data" / "combined"
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Folder containing all processed CSVs
data_dir = Path("data/processed")

# Find all *_events.csv files
csv_files = sorted(data_dir.glob("defcon*_events.csv"))

# Read and concatenate them
df_all = pl.concat([pl.read_csv(f) for f in csv_files])

#  Write combined file for analysis
df_all.write_csv(f"{RAW_DIR}/defcon_all_events.csv")
