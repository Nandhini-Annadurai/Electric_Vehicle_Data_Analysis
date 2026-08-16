from pathlib import Path
import argparse
import sqlite3

import pandas as pd


QUERIES = {
    "ev_type_counts": """
        SELECT "Electric Vehicle Type" AS ev_type, COUNT(*) AS count
        FROM ev_population
        GROUP BY ev_type
        ORDER BY count DESC;
    """,
    "top_makes": """
        SELECT Make, COUNT(*) AS count
        FROM ev_population
        GROUP BY Make
        ORDER BY count DESC
        LIMIT 15;
    """,
    "top_models": """
        SELECT Make, Model, COUNT(*) AS count
        FROM ev_population
        GROUP BY Make, Model
        ORDER BY count DESC
        LIMIT 15;
    """,
    "county_counts": """
        SELECT County, COUNT(*) AS count
        FROM ev_population
        GROUP BY County
        ORDER BY count DESC
        LIMIT 15;
    """,
    "year_trend": """
        SELECT "Model Year" AS model_year, COUNT(*) AS count
        FROM ev_population
        GROUP BY model_year
        ORDER BY model_year;
    """,
    "cafv_eligibility": """
        SELECT
            "Clean Alternative Fuel Vehicle (CAFV) Eligibility" AS cafv,
            COUNT(*) AS count
        FROM ev_population
        GROUP BY cafv
        ORDER BY count DESC;
    """,
    "top_utilities": """
        SELECT "Electric Utility" AS utility, COUNT(*) AS count
        FROM ev_population
        GROUP BY utility
        ORDER BY count DESC
        LIMIT 10;
    """,
    "avg_range_by_make": """
        SELECT
            Make,
            ROUND(AVG("Electric Range"), 1) AS avg_range,
            COUNT(*) AS count
        FROM ev_population
        WHERE "Electric Range" IS NOT NULL
          AND "Electric Range" > 0
        GROUP BY Make
        HAVING COUNT(*) >= 50
        ORDER BY avg_range DESC
        LIMIT 15;
    """,
}


def run_analysis(cleaned_csv, database, output_dir):
    cleaned_csv = Path(cleaned_csv)
    database = Path(database)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    database.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(cleaned_csv, low_memory=False)

    with sqlite3.connect(database) as connection:
        df.to_sql("ev_population", connection, if_exists="replace", index=False)

        for name, query in QUERIES.items():
            result = pd.read_sql_query(query, connection)
            output = output_dir / f"sql_{name}.csv"
            result.to_csv(output, index=False)
            print(f"{name}: {len(result)} rows -> {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run EV summary queries in SQLite.")
    parser.add_argument("cleaned_csv", type=Path)
    parser.add_argument("database", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    run_analysis(args.cleaned_csv, args.database, args.output_dir)
