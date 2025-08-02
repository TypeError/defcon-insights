#!/usr/bin/env python3

import argparse
import json
from pathlib import Path

import polars as pl

# Directories
ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT_DIR / "data" / "processed"
RAW_DIR.mkdir(parents=True, exist_ok=True)


def tag_id_label(defcon: int):
    with open(f"data/raw/defcon{defcon}/tagtypes.json") as f:
        data = json.load(f)

    id_to_label = {}

    for tagtype in data:
        tags = (
            tagtype.get("fields", {})
            .get("tags", {})
            .get("arrayValue", {})
            .get("values", [])
        )
        for tag in tags:
            fields = tag.get("mapValue", {}).get("fields", {})
            tag_id = int(fields.get("id", {}).get("integerValue", 0))
            label = fields.get("label", {}).get("stringValue", "")
            id_to_label[tag_id] = label

    return id_to_label


def location_id_name(defcon: int):
    with open(f"data/raw/defcon{defcon}/locations.json") as f:
        data = json.load(f)

    id_to_name = {}

    for location in data:
        fields = location.get("fields", {})
        location_id = int(fields.get("id", {}).get("integerValue", 0))
        name = fields.get("short_name", {}).get("stringValue", "")
        id_to_name[location_id] = name

    return id_to_name


def process_events(defcon: int):
    # Load the JSON file
    with open(f"data/raw/defcon{defcon}/events.json") as f:
        data = json.load(f)

    locations = location_id_name(defcon)
    tags = tag_id_label(defcon)

    events = []

    for event in data:
        fields = event.get("fields", {})
        if not fields:
            continue
        title = fields.get("title", {}).get("stringValue")
        begin_timestamp = fields.get("begin_timestamp", {}).get("timestampValue")
        end_timestamp = fields.get("end_timestamp", {}).get("timestampValue")
        location = locations.get(
            int(
                fields.get("location", {})
                .get("mapValue", {})
                .get("fields", {})
                .get("id", {})
                .get("integerValue", 0)
            ),
        )
        event_type = tags.get(
            int(
                fields.get("type", {})
                .get("mapValue", {})
                .get("fields", {})
                .get("id", {})
                .get("integerValue", 0)
            ),
            "",
        )

        tag_ids = ",".join(
            [
                tags.get(int(tag_id.get("integerValue"), 0), "")
                for tag_id in fields.get("tag_ids", {})
                .get("arrayValue", {})
                .get("values", [])
                if tags.get(int(tag_id.get("integerValue"), 0), "") != ""
            ]
        )

        description = fields.get("description", {}).get("stringValue", "")

        events.append(
            {
                "title": title,
                "begin_timestamp": begin_timestamp,
                "end_timestamp": end_timestamp,
                "location": location,
                "event_type": event_type,
                "tags": tag_ids,
                "description": description,
            }
        )

    return events


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--defcon", type=int, help="DEF CON (e.g. 33)", required=True)
    args = parser.parse_args()
    defcon = args.defcon

    events = process_events(defcon)
    events_df = pl.DataFrame(events).with_columns(pl.lit(defcon).alias("defcon"))
    out_path = RAW_DIR / f"defcon{defcon}_events.csv"
    events_df.write_csv(out_path)


if __name__ == "__main__":
    main()
