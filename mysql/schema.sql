CREATE DATABASE IF NOT EXISTS ev_analysis
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE ev_analysis;

DROP TABLE IF EXISTS ev_population;

CREATE TABLE ev_population (
    vin_10               VARCHAR(10),
    county               VARCHAR(100),
    city                 VARCHAR(100),
    state                VARCHAR(5),
    postal_code          INT,
    model_year           SMALLINT,
    make                 VARCHAR(50),
    model                VARCHAR(100),
    ev_type              VARCHAR(60),
    cafv_eligibility     VARCHAR(120),
    electric_range       SMALLINT,
    base_msrp             INT,
    legislative_district SMALLINT,
    dol_vehicle_id       BIGINT,
    vehicle_location     VARCHAR(60),
    electric_utility     VARCHAR(255),
    census_tract_2020    BIGINT,
    latitude             DECIMAL(9,6),
    longitude            DECIMAL(9,6),
    INDEX idx_make (make),
    INDEX idx_county (county),
    INDEX idx_model_year (model_year),
    INDEX idx_ev_type (ev_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
