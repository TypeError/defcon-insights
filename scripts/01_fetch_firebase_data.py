#!/usr/bin/env python3

import requests
import json
from pathlib import Path
import argparse

# ----- CONFIGURATION -----
PROJECT_ID = "junctor-hackertracker"
DATABASE = "(default)"
PAGE_SIZE = 300  # max per Firestore limits

# Collections to fetch (add or remove as needed)
COLLECTIONS = [
    "events",
    "locations",
    "tagtypes",
]


def fetch_collection(defcon: int, collection: str, page_size: int = PAGE_SIZE) -> list:
    """
    Fetch all documents in a Firestore collection via REST, handling pagination.
    """
    conf_code = f"DEFCON{defcon}"

    firestore_base = (
        f"https://firestore.googleapis.com/v1/projects/{PROJECT_ID}"
        f"/databases/{DATABASE}/documents/conferences/{conf_code}"
    )

    docs = []
    params = {"pageSize": page_size}
    next_page = None

    url = f"{firestore_base}/{collection}"
    print(f"Fetching '{collection}' from {conf_code}...")

    while True:
        if next_page:
            params["pageToken"] = next_page

        resp = requests.get(url, params=params)
        resp.raise_for_status()
        data = resp.json()

        batch = data.get("documents", [])
        docs.extend(batch)
        print(f"  - Retrieved {len(batch)} docs (total {len(docs)})")

        next_page = data.get("nextPageToken")
        if not next_page:
            break

    return docs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--defcon", type=int, help="DEF CON (e.g. 33)", required=True)
    args = parser.parse_args()
    defcon = args.defcon

    root_dir = Path(__file__).resolve().parent.parent
    raw_dir = root_dir / "data" / "raw" / f"defcon{defcon}"
    raw_dir.mkdir(parents=True, exist_ok=True)

    for coll in COLLECTIONS:
        records = fetch_collection(defcon, coll)
        out_path = raw_dir / f"{coll}.json"
        with open(out_path, "w") as f:
            json.dump(records, f, separators=(",", ":"))
        print(f"Saved {len(records)} '{coll}' docs to {out_path}\n")


if __name__ == "__main__":
    main()
