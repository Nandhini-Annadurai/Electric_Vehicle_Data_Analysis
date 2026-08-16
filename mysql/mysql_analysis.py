from pathlib import Path
import argparse

import mysql.connector
import pandas as pd


QUERIES = {
    "ev_type_counts": """
        SELECT ev_type, COUNT(*) AS vehicle_count
        FROM ev_population GROUP BY ev_type ORDER BY vehicle_count DESC;
    """,
    "top_makes": """
        SELECT make, COUNT(*) AS vehicle_count
        FROM ev_population GROUP BY make ORDER BY vehicle_count DESC LIMIT 15;
    """,
    "top_models": """
        SELECT make, model, COUNT(*) AS vehicle_count
        FROM ev_population
        GROUP BY make, model
        ORDER BY vehicle_count DESC
        LIMIT 15;
    """,
    "county_counts": """
        SELECT county, COUNT(*) AS vehicle_count
        FROM ev_population
        GROUP BY county
        ORDER BY vehicle_count DESC
        LIMIT 15;
    """,
    "year_trend": """
        SELECT model_year, COUNT(*) AS vehicle_count
        FROM ev_population
        GROUP BY model_year
        ORDER BY model_year;
    """,
    "cafv_eligibility": """
        SELECT cafv_eligibility, COUNT(*) AS vehicle_count
        FROM ev_population
        GROUP BY cafv_eligibility
        ORDER BY vehicle_count DESC;
    """,
    "top_utilities": """
        SELECT electric_utility, COUNT(*) AS vehicle_count
        FROM ev_population
        GROUP BY electric_utility
        ORDER BY vehicle_count DESC
        LIMIT 10;
    """,
    "avg_range_by_make": """
        SELECT make, ROUND(AVG(electric_range), 1) AS avg_range,
               COUNT(*) AS vehicle_count
        FROM ev_population
        WHERE electric_range IS NOT NULL AND electric_range > 0
        GROUP BY make
        HAVING COUNT(*) >= 50
        ORDER BY avg_range DESC
        LIMIT 15;
    """,
}


def load_csv(connection, csv_path, batch_size=5000):
    df = pd.read_csv(csv_path)
    df = df.rename(columns={
        "VIN (1-10)": "vin_10",
        "County": "county",
        "City": "city",
        "State": "state",
        "Postal Code": "postal_code",
        "Model Year": "model_year",
        "Make": "make",
        "Model": "model",
        "Electric Vehicle Type": "ev_type",
        "Clean Alternative Fuel Vehicle (CAFV) Eligibility": "cafv_eligibility",
        "Electric Range": "electric_range",
        "Base MSRP": "base_msrp",
        "Legislative District": "legislative_district",
        "DOL Vehicle ID": "dol_vehicle_id",
        "Vehicle Location": "vehicle_location",
        "Electric Utility": "electric_utility",
        "2020 Census Tract": "census_tract_2020",
        "Latitude": "latitude",
        "Longitude": "longitude",
    })
    df = df.where(pd.notnull(df), None)

    columns = list(df.columns)
    placeholders = ", ".join(["%s"] * len(columns))
    statement = (
        f"INSERT INTO ev_population ({', '.join(columns)}) "
        f"VALUES ({placeholders})"
    )

    cursor = connection.cursor()
    rows = df.values.tolist()

    for start in range(0, len(rows), batch_size):
        batch = rows[start:start + batch_size]
        cursor.executemany(statement, batch)
        connection.commit()
        print(f"Loaded {min(start + batch_size, len(rows)):,} / {len(rows):,}")

    cursor.close()


def export_results(connection, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    for name, query in QUERIES.items():
        result = pd.read_sql(query, connection)
        result.to_csv(output_dir / f"mysql_{name}.csv", index=False)
        print(f"Wrote mysql_{name}.csv")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load and analyse the EV data in MySQL.")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=3306)
    parser.add_argument("--user", required=True)
    parser.add_argument("--password", required=True)
    parser.add_argument("--database", default="ev_analysis")
    parser.add_argument("--csv", default="../cleaned_data/EV_Population_Cleaned.csv")
    parser.add_argument("--output", default="../cleaned_data")
    parser.add_argument("--load", action="store_true")
    args = parser.parse_args()

    connection = mysql.connector.connect(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        database=args.database,
    )

    try:
        if args.load:
            load_csv(connection, args.csv)
        export_results(connection, args.output)
    finally:
        connection.close()
