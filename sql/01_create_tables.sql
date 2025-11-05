-- 01_create_tables.sql
-- This script creates normalized tables for the property ETL

-- =========================
-- 1. property table
-- =========================
CREATE TABLE IF NOT EXISTS property (
    property_id INT AUTO_INCREMENT PRIMARY KEY,
    property_title VARCHAR(255),
    address VARCHAR(255),
    market VARCHAR(100),
    flood VARCHAR(50),
    street_address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(50),
    zip VARCHAR(20),
    property_type VARCHAR(50),
    highway VARCHAR(50),
    train VARCHAR(50),
    tax_rate DECIMAL(5,2),
    sqft_basement INT,
    htw VARCHAR(10),
    pool VARCHAR(10),
    commercial VARCHAR(10),
    water VARCHAR(50),
    sewage VARCHAR(50),
    year_built INT,
    sqft_mu INT,
    sqft_total VARCHAR(50),
    parking VARCHAR(50),
    bed INT,
    bath INT,
    basement_yes_no VARCHAR(10),
    layout VARCHAR(50),
    rent_restricted VARCHAR(10),
    neighborhood_rating INT,
    latitude DECIMAL(9,6),
    longitude DECIMAL(9,6),
    subdivision VARCHAR(100),
    taxes DECIMAL(10,2),
    school_average DECIMAL(5,2)
);

-- =========================
-- 2. leads table
-- =========================
CREATE TABLE IF NOT EXISTS leads (
    lead_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    reviewed_status VARCHAR(50),
    most_recent_status VARCHAR(50),
    source VARCHAR(50),
    occupancy VARCHAR(20),
    net_yield DECIMAL(5,2),
    irr DECIMAL(5,2),
    selling_reason VARCHAR(255),
    seller_retained_broker VARCHAR(255),
    final_reviewer VARCHAR(255),
    FOREIGN KEY (property_id) REFERENCES property(property_id)
);

-- =========================
-- 3. valuation table
-- =========================
CREATE TABLE IF NOT EXISTS valuation (
    valuation_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    list_price DECIMAL(12,2),
    previous_rent DECIMAL(10,2),
    zestimate DECIMAL(12,2),
    arv DECIMAL(12,2),
    expected_rent DECIMAL(10,2),
    rent_zestimate DECIMAL(10,2),
    low_fmr DECIMAL(10,2),
    high_fmr DECIMAL(10,2),
    redfin_value DECIMAL(12,2),
    FOREIGN KEY (property_id) REFERENCES property(property_id)
);

-- =========================
-- 4. HOA table
-- =========================
CREATE TABLE IF NOT EXISTS hoa (
    hoa_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    hoa_fee DECIMAL(10,2),
    hoa_flag VARCHAR(10),
    FOREIGN KEY (property_id) REFERENCES property(property_id)
);

-- =========================
-- 5. rehab table
-- =========================
CREATE TABLE IF NOT EXISTS rehab (
    rehab_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    underwriting_rehab DECIMAL(12,2),
    rehab_calculation DECIMAL(12,2),
    paint VARCHAR(10),
    flooring_flag VARCHAR(10),
    foundation_flag VARCHAR(10),
    roof_flag VARCHAR(10),
    hvac_flag VARCHAR(10),
    kitchen_flag VARCHAR(10),
    bathroom_flag VARCHAR(10),
    appliances_flag VARCHAR(10),
    windows_flag VARCHAR(10),
    landscaping_flag VARCHAR(10),
    trashout_flag VARCHAR(10),
    FOREIGN KEY (property_id) REFERENCES property(property_id)
);

-- =========================
-- 6. taxes table
-- =========================
CREATE TABLE IF NOT EXISTS taxes (
    tax_id INT AUTO_INCREMENT PRIMARY KEY,
    property_id INT,
    taxes DECIMAL(12,2),
    FOREIGN KEY (property_id) REFERENCES property(property_id)
);
