#!/usr/bin/env bash
set -euo pipefail

# Array of DEF CON numbers
defcons=(32 33)

# Loop over each DEF CON year
for dc in "${defcons[@]}"; do
  echo "Fetching raw data for DEF CON $dc..."
  python scripts/01_fetch_firebase_data.py --defcon "$dc"

  echo "Processing data for DEF CON $dc..."
  python scripts/02_process_defcon_data.py --defcon "$dc"
done

# Combine all processed CSVs
echo "Combining all years..."
python scripts/03_combine_all_years.py

echo "DEF CON Insights Pipeline complete."