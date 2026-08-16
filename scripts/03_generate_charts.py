from pathlib import Path
import argparse

import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd


def save_chart(fig, output_dir, name):
    output_dir.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(output_dir / f"{name}.png", dpi=150)
    plt.close(fig)


def generate_charts(data_dir, output_dir):
    data_dir = Path(data_dir)
    output_dir = Path(output_dir)

    # EV type split
    df = pd.read_csv(data_dir / "sql_ev_type_counts.csv")
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(df["count"], labels=df["ev_type"], autopct="%1.1f%%", startangle=90)
    ax.set_title("EV Population by Type")
    save_chart(fig, output_dir, "01_ev_type_distribution")

    # Top makes
    df = pd.read_csv(data_dir / "sql_top_makes.csv").head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df["Make"], df["count"])
    ax.set_title("Top 10 EV Makes by Registration Count")
    ax.set_ylabel("Vehicles")
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    plt.xticks(rotation=45, ha="right")
    save_chart(fig, output_dir, "02_top_10_makes")

    # Top models
    df = pd.read_csv(data_dir / "sql_top_models.csv").head(10).copy()
    df["label"] = df["Make"] + " " + df["Model"]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(df["label"][::-1], df["count"][::-1])
    ax.set_title("Top 10 EV Models by Registration Count")
    ax.set_xlabel("Vehicles")
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    save_chart(fig, output_dir, "03_top_10_models")

    # Top counties
    df = pd.read_csv(data_dir / "sql_county_counts.csv").head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df["County"], df["count"])
    ax.set_title("Top 10 Counties by EV Registration Count")
    ax.set_ylabel("Vehicles")
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    plt.xticks(rotation=45, ha="right")
    save_chart(fig, output_dir, "04_top_10_counties")

    # Model-year trend
    df = pd.read_csv(data_dir / "sql_year_trend.csv")
    df = df[df["model_year"].between(2011, 2025)]
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(df["model_year"], df["count"], marker="o")
    ax.set_title("EV Registrations by Model Year")
    ax.set_xlabel("Model Year")
    ax.set_ylabel("Vehicles")
    ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    save_chart(fig, output_dir, "05_registrations_by_year")

    # CAFV eligibility
    df = pd.read_csv(data_dir / "sql_cafv_eligibility.csv")
    fig, ax = plt.subplots(figsize=(6.5, 6.5))
    ax.pie(df["count"], labels=df["cafv"], autopct="%1.1f%%", startangle=90)
    ax.set_title("CAFV Eligibility")
    save_chart(fig, output_dir, "06_cafv_eligibility")

    # Average range by make
    df = pd.read_csv(data_dir / "sql_avg_range_by_make.csv")
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(df["Make"], df["avg_range"])
    ax.set_title("Average Electric Range by Make")
    ax.set_ylabel("Average range (miles)")
    plt.xticks(rotation=45, ha="right")
    save_chart(fig, output_dir, "07_avg_range_by_make")

    # Top utilities
    df = pd.read_csv(data_dir / "sql_top_utilities.csv").head(8).copy()
    df["label"] = df["utility"].str.slice(0, 40)
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.barh(df["label"][::-1], df["count"][::-1])
    ax.set_title("Top Electric Utility Service Territories")
    ax.set_xlabel("Vehicles")
    ax.xaxis.set_major_formatter(mticker.StrMethodFormatter("{x:,.0f}"))
    save_chart(fig, output_dir, "08_top_utilities")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create project charts from SQL outputs.")
    parser.add_argument("data_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    generate_charts(args.data_dir, args.output_dir)
