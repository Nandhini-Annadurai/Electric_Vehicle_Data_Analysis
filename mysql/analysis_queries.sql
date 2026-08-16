USE ev_analysis;

-- EV type distribution
SELECT ev_type, COUNT(*) AS vehicle_count
FROM ev_population
GROUP BY ev_type
ORDER BY vehicle_count DESC;

-- Leading makes
SELECT make, COUNT(*) AS vehicle_count
FROM ev_population
GROUP BY make
ORDER BY vehicle_count DESC
LIMIT 15;

-- Leading models
SELECT make, model, COUNT(*) AS vehicle_count
FROM ev_population
GROUP BY make, model
ORDER BY vehicle_count DESC
LIMIT 15;

-- Leading counties
SELECT county, COUNT(*) AS vehicle_count
FROM ev_population
GROUP BY county
ORDER BY vehicle_count DESC
LIMIT 15;

-- Registrations by model year
SELECT model_year, COUNT(*) AS vehicle_count
FROM ev_population
GROUP BY model_year
ORDER BY model_year;

-- CAFV eligibility
SELECT cafv_eligibility, COUNT(*) AS vehicle_count
FROM ev_population
GROUP BY cafv_eligibility
ORDER BY vehicle_count DESC;

-- Leading electric utilities
SELECT electric_utility, COUNT(*) AS vehicle_count
FROM ev_population
GROUP BY electric_utility
ORDER BY vehicle_count DESC
LIMIT 10;

-- Average electric range by make, using makes with at least 50 vehicles
SELECT
    make,
    ROUND(AVG(electric_range), 1) AS avg_range,
    COUNT(*) AS vehicle_count
FROM ev_population
WHERE electric_range IS NOT NULL
  AND electric_range > 0
GROUP BY make
HAVING COUNT(*) >= 50
ORDER BY avg_range DESC
LIMIT 15;
