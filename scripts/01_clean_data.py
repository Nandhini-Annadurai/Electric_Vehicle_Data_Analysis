from pathlib import Path
import argparse
import re

import numpy as np
import pandas as pd


NUMERIC_COLUMNS = [
    "Model Year",
    "Electric Range",
    "Base MSRP",
    "Legislative District",
    "DOL Vehicle ID",
    "2020 Census Tract",
    "Postal Code",
]


def parse_point(value):
    if not isinstance(value, str):
        return np.nan, np.nan

    match = re.match(
        r"POINT\s*\(\s*(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s*\)",
        value,
    )
    if not match:
        return np.nan, np.nan

    longitude, latitude = map(float, match.groups())
    return latitude, longitude


def clean_data(source_csv, output_csv):
    df = pd.read_csv(source_csv, dtype=str, low_memory=False)
    print(f"Rows read: {len(df):,}")

    df.columns = df.columns.str.strip()

    for column in NUMERIC_COLUMNS:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")

    if "Vehicle Location" in df.columns:
        coordinates = df["Vehicle Location"].map(parse_point)
        df["Latitude"] = coordinates.map(lambda value: value[0])
        df["Longitude"] = coordinates.map(lambda value: value[1])

    text_columns = df.select_dtypes(include="object").columns
    for column in text_columns:
        df[column] = df[column].str.strip()
        df[column] = df[column].replace({"": np.nan, "nan": np.nan})

    before = len(df)
    df = df.drop_duplicates()
    print(f"Exact duplicates removed: {before - len(df):,}")

    before = len(df)
    required = ["VIN (1-10)", "Make", "Model", "Model Year"]
    df = df.dropna(subset=required)
    print(f"Rows missing required fields removed: {before - len(df):,}")

    if "Model Year" in df:
        df = df[df["Model Year"].between(1997, 2026)]

    if "Electric Range" in df:
        df.loc[df["Electric Range"] < 0, "Electric Range"] = np.nan

    if "Base MSRP" in df:
        df.loc[df["Base MSRP"] <= 0, "Base MSRP"] = np.nan

    for column in ("Make", "Model"):
        if column in df:
            df[column] = df[column].str.upper()

    output_csv = Path(output_csv)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_csv, index=False)

    print(f"Rows written: {len(df):,}")
    print(f"Output: {output_csv}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean the EV population CSV.")
    parser.add_argument("source_csv", type=Path)
    parser.add_argument("output_csv", type=Path)
    args = parser.parse_args()
    clean_data(args.source_csv, args.output_csv)
