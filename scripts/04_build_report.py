from pathlib import Path
import argparse
from datetime import date

import pandas as pd


def build_report(data_dir, output_file):
    data_dir = Path(data_dir)
    output_file = Path(output_file)

    clean = pd.read_csv(data_dir / "EV_Population_Cleaned.csv", low_memory=False)
    ev_type = pd.read_csv(data_dir / "sql_ev_type_counts.csv")
    top_makes = pd.read_csv(data_dir / "sql_top_makes.csv")
    top_models = pd.read_csv(data_dir / "sql_top_models.csv")
    counties = pd.read_csv(data_dir / "sql_county_counts.csv")
    cafv = pd.read_csv(data_dir / "sql_cafv_eligibility.csv")
    avg_range = pd.read_csv(data_dir / "sql_avg_range_by_make.csv")

    total = int(len(clean))
    bev = int(ev_type.loc[ev_type.ev_type.str.contains("BEV", na=False), "count"].iloc[0])
    phev = int(ev_type.loc[ev_type.ev_type.str.contains("PHEV", na=False), "count"].iloc[0])

    eligible = cafv.loc[
        cafv.cafv.str.contains("Eligible", case=False, na=False), "count"
    ]
    eligible_count = int(eligible.iloc[0]) if not eligible.empty else 0

    lines = [
        "# Electric Vehicle Population — Analysis Summary",
        "",
        f"_Report date: {date.today().isoformat()}_",
        "",
        "## Data preparation",
        f"- Input records: {total:,}",
        f"- Records in the cleaned dataset: {total:,}",
        "- Text fields were trimmed and Make/Model values were standardized to uppercase.",
        "- Numeric fields were converted to numeric types where applicable.",
        "- Vehicle Location coordinates were split into Latitude and Longitude.",
        "- Exact duplicates and rows without VIN, Make, Model, or Model Year were removed.",
        "- Model years outside 1997–2026 were excluded.",
        "- Negative electric range values and non-positive MSRP values were set to missing.",
        "",
        "## Main results",
        f"- BEV: {bev:,} ({bev / total:.1%})",
        f"- PHEV: {phev:,} ({phev / total:.1%})",
        f"- Leading make: {top_makes.iloc[0]['Make']} ({int(top_makes.iloc[0]['count']):,})",
        f"- Leading model: {top_models.iloc[0]['Make']} {top_models.iloc[0]['Model']} ({int(top_models.iloc[0]['count']):,})",
        f"- Leading county: {counties.iloc[0]['County']} ({int(counties.iloc[0]['count']):,})",
        f"- CAFV eligible: {eligible_count:,} ({eligible_count / total:.1%})",
        f"- Highest average range among makes with at least 50 vehicles: "
        f"{avg_range.iloc[0]['Make']} ({avg_range.iloc[0]['avg_range']} miles)",
        "",
        "## Power BI",
        "The supplied EV_DASHBOARD.pbix is retained in the package as the dashboard file.",
        "Open it in Power BI Desktop to inspect or refresh the report.",
        "",
        "## Charts",
    ]

    for name, description in [
        ("01_ev_type_distribution.png", "EV type distribution"),
        ("02_top_10_makes.png", "Top 10 makes"),
        ("03_top_10_models.png", "Top 10 models"),
        ("04_top_10_counties.png", "Top 10 counties"),
        ("05_registrations_by_year.png", "Registrations by model year"),
        ("06_cafv_eligibility.png", "CAFV eligibility"),
        ("07_avg_range_by_make.png", "Average electric range by make"),
        ("08_top_utilities.png", "Top electric utilities"),
    ]:
        lines.append(f"- `{name}` — {description}")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Report written to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the EV analysis summary.")
    parser.add_argument("data_dir", type=Path)
    parser.add_argument("output_file", type=Path)
    args = parser.parse_args()
    build_report(args.data_dir, args.output_file)
