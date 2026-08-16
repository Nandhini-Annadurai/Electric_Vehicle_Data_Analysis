
# Electric Vehicle Data Analysis

## 📌 Project Overview

I worked on this project to explore electric vehicle registration data and understand what the data says about EV adoption, popular manufacturers and models, vehicle range, location, and CAFV eligibility.

The project covers the full analysis process, starting with cleaning the raw data in Python, followed by SQL analysis and visualisation, and finally presenting the main findings through a Power BI dashboard.

The main goal was to take a large and fairly messy EV dataset and turn it into something that is easier to analyse and understand.

## 🧠 Objectives

* Clean and prepare the EV registration dataset for analysis
* Find the manufacturers and models with the highest number of registrations
* Compare Battery Electric Vehicles and Plug-in Hybrid Electric Vehicles
* Look at how registrations vary by model year
* Understand where EV registrations are concentrated geographically
* Compare the average electric range across manufacturers
* Analyse CAFV eligibility within the dataset
* Explore the electric utilities associated with registered vehicles
* Build a Power BI dashboard to bring the analysis together

## 🧰 Tools Used

* **Python** – data cleaning, preparation, analysis, and charts
* **Pandas** – working with and transforming the dataset
* **NumPy** – numerical operations and data handling
* **Matplotlib** – creating analysis charts
* **SQL** – querying and summarising the data
* **MySQL** – database-based analysis
* **SQLite** – local database analysis
* **Power BI** – dashboard and interactive visualisation

## 📊 What I Analysed

### EV Types

I compared the two main EV categories in the dataset:

* Battery Electric Vehicles (BEV)
* Plug-in Hybrid Electric Vehicles (PHEV)

### Manufacturers and Models

I looked at registration counts by manufacturer and then drilled down into individual models to see which vehicles appear most often in the dataset.

### Model Year

The model-year analysis shows how the number of registered EVs changes across different vehicle years.

### Location

The dataset contains county, city, and location information. I used these fields to understand where EV registrations are concentrated.

### Electric Range

I also looked at the recorded electric range and calculated average range values for manufacturers with enough records to make the comparison useful.

### CAFV Eligibility

The project includes an analysis of the Clean Alternative Fuel Vehicle (CAFV) eligibility field to see how vehicles are distributed across the available eligibility categories.

### Electric Utilities

The electric utility field was analysed to identify the utility service territories associated with the largest number of EV registrations.

## 📈 Analysis Approach

The project follows a simple workflow:

```text
Raw EV Data
     ↓
Python Data Cleaning
     ↓
Cleaned Dataset
     ↓
SQL Analysis
     ↓
Charts & Analysis
     ↓
Power BI Dashboard
     ↓
Final Insights
```

During data cleaning, I removed duplicate records, handled missing values, converted numeric fields, cleaned text values, and separated latitude and longitude from the vehicle-location field.

After cleaning the data, I used SQL to produce summaries for manufacturers, models, counties, model years, EV types, CAFV eligibility, electric utilities, and electric range.

The resulting summaries were then used for the charts and dashboard.

## 📊 Key Results

Some of the main results from the cleaned dataset were:

* **150,482** records in the cleaned dataset
* **BEVs:** 116,807 records
* **PHEVs:** 33,675 records
* **Tesla:** 68,983 registrations
* **Tesla Model Y:** 28,502 registrations
* **King Country:** 79,075 registrations
* **CAFV eligible:** 62,951 records
* **Tesla average electric range:** approximately 240.5 miles among the analysed records

These numbers give a quick picture of how strongly certain manufacturers, models, and locations are represented in the dataset.


## ⚠️ Limitations

There are a few things to keep in mind when interpreting the results.

The dataset contains registration records rather than a complete count of every EV on the road. Because of this, the numbers should be treated as registration data rather than total EV ownership.

Some fields contain missing or incomplete values, so calculations such as electric range and MSRP depend on the records where those values are available.

The geographic results are also limited to the locations included in the source dataset.

Finally, the CAFV classification comes directly from the source data, so the analysis reflects the classifications provided in that dataset.

## 🚀 Running the Project

Install the Python dependencies:

```bash
pip install pandas numpy matplotlib
```

Run the Python workflow:

```bash
python scripts/01_clean_data.py
python scripts/02_sql_analysis.py
python scripts/03_generate_charts.py
python scripts/04_build_report.py
```

For the MySQL analysis, start with:

```text
mysql/schema.sql
```

Then load the cleaned data:

```text
mysql/load_data.sql
```

The analysis queries are available in:

```text
mysql/analysis_queries.sql
```

The Power BI dashboard is located at:

```text
powerbi/EV_DASHBOARD.pbix
```

