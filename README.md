# DEF CON Insights

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**DEF CON Insights** is a data analysis project that transforms DEF CON conference data into clean, structured formats for deeper exploration and visualization.

This repository currently provides scripts to fetch and process structured content (events, tags, speakers, locations) from DEF CON’s Firebase backend. A Quarto site with published statistics, trends, and visual insights is planned.

## 🧪 Current Capabilities

- Fetch raw data from DEF CON’s Firebase/Firestore  
- Normalize and flatten nested fields into analysis-ready tables  
- Combine multiple years for cross-year comparisons  

## 📁 Project Structure

```bash
scripts/
├── 01_fetch_firebase_data.py     # Downloads raw JSON data for a given DEF CON year
├── 02_process_defcon_data.py     # Transforms verbose Firestore exports into flat CSV/JSON
├── 03_combine_all_years.py       # Merges all processed files into a single dataset

run_pipeline.sh                    # Orchestrates the full data pipeline for selected DEF CON years
```

## 🚀 Usage

You can run the full pipeline for DEF CON 32 and 33 using:

```bash
bash run_pipeline.sh
```

This will:
1. Fetch raw data into `data/raw/`
1. Process cleaned files into `data/processed/`
1. Merge all processed years into `data/combined/defcon_all_events.csv`

## 🔧 Tools & Technologies

This project leverages:

- **[Polars](https://pola.rs/)** for fast, multi-threaded DataFrame transformations  
- **[Requests](https://docs.python-requests.org/)** to fetch raw JSON from Firebase  
- **[Quarto](https://quarto.org/)** (coming) for analysis notebooks and site publishing  
- **[Plotnine](https://plotnine.org/)** (coming) for grammar-of-graphics plotting and visual insights  


## 📄 License

This project is MIT-licensed. See [LICENSE](LICENSE) for details.