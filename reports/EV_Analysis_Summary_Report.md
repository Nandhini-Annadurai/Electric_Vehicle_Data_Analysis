# Electric Vehicle Population — Analysis Summary

## Data preparation

The cleaned dataset contains 150,482 records.

The cleaning process:
- trims whitespace in text columns;
- standardizes Make and Model values to uppercase;
- converts numeric columns to numeric types;
- separates latitude and longitude from Vehicle Location;
- removes exact duplicate rows;
- removes rows missing VIN, Make, Model, or Model Year;
- keeps model years from 1997 through 2026;
- replaces negative electric-range values with missing values;
- replaces non-positive MSRP values with missing values.

## Main results

- BEV: 116,807 (77.6%)
- PHEV: 33,675 (22.4%)
- Leading make: TESLA (68,983)
- Leading model: TESLA MODEL Y (28,502)
- Leading county: King (79,075)
- CAFV eligible: 62,951 (41.8%)
- Highest average range among makes with at least 50 vehicles: TESLA (240.5 miles)

## Charts

The `charts` directory contains eight charts covering EV type, manufacturers, models, counties, model-year registrations, CAFV eligibility, average range, and electric utilities.

## Power BI dashboard

`EV_DASHBOARD.pbix` is included as the dashboard deliverable. It can be opened and refreshed in Power BI Desktop.
