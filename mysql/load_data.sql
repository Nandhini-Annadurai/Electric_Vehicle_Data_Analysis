USE ev_analysis;

LOAD DATA LOCAL INFILE '../cleaned_data/EV_Population_Cleaned.csv'
INTO TABLE ev_population
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    vin_10,
    county,
    city,
    state,
    @postal_code,
    @model_year,
    make,
    model,
    ev_type,
    cafv_eligibility,
    @electric_range,
    @base_msrp,
    @legislative_district,
    @dol_vehicle_id,
    vehicle_location,
    electric_utility,
    @census_tract_2020,
    @latitude,
    @longitude
)
SET
    postal_code = NULLIF(@postal_code, ''),
    model_year = NULLIF(@model_year, ''),
    electric_range = NULLIF(@electric_range, ''),
    base_msrp = NULLIF(@base_msrp, ''),
    legislative_district = NULLIF(@legislative_district, ''),
    dol_vehicle_id = NULLIF(@dol_vehicle_id, ''),
    census_tract_2020 = NULLIF(@census_tract_2020, ''),
    latitude = NULLIF(@latitude, ''),
    longitude = NULLIF(@longitude, '');

SELECT COUNT(*) AS rows_loaded
FROM ev_population;
