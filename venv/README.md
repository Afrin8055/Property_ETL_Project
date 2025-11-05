# Property ETL Project

## Folder Structure

data_engineer_assessment/
├─ data/
│ ├─ fake_property_data_new.json
│ └─ Field Config.xlsx
├─ scripts/
│ ├─ etl_load_data.py
│ └─ validate_data.py
├─ sql/
│ └─ create_tables.sql
├─ requirements.txt
└─ README.md

sql
Copy code

---

## Problem Statement

You are provided with a raw JSON file containing property records in the `data/` folder. Each row relates to a property but contains multiple unrelated attributes (property details, HOA data, rehab estimates, valuations, taxes, leads, etc.).  

The database is **not normalized** and lacks relational structure.  

Your task was to:

1. Normalize the data.
2. Build a Python ETL script to read, clean, transform, and load data into MySQL.
3. Use primary keys and foreign keys to capture relationships.
4. Provide SQL scripts to create the tables manually.
5. Document all steps and instructions for reproducibility.

---

## **Database Schema & Design**

The database design uses **`property` as the central table**, with all other tables referencing `property_id` as a foreign key. Each nested table can have multiple rows per property.  

| Table       | Description                                       | PK / FK                       |
|------------|---------------------------------------------------|-------------------------------|
| `property` | Central table with main property attributes      | `property_id` PK             |
| `leads`    | Lead info for properties                          | `lead_id` PK, `property_id` FK → property(property_id) |
| `valuation`| Valuation data for properties                     | `valuation_id` PK, `property_id` FK |
| `hoa`      | HOA details                                      | `hoa_id` PK, `property_id` FK |
| `rehab`    | Rehab estimates and flags                         | `rehab_id` PK, `property_id` FK |
| `taxes`    | Property taxes                                   | `tax_id` PK, `property_id` FK |

### Design Decisions

- Property table holds all general property attributes.
- Nested tables (valuation, rehab, HOA, taxes, leads) are separated for normalization.
- Foreign keys maintain referential integrity.
- ETL script dynamically adds missing columns if new fields appear in JSON.
- Tables allow multiple entries per property in nested tables.

---

## **SQL Script – `sql/create_tables.sql`**

Contains all CREATE TABLE statements to manually create the normalized schema.  

```sql
-- Example: Property table
CREATE TABLE property (
    property_id INT AUTO_INCREMENT PRIMARY KEY,
    property_title VARCHAR(255),
    address VARCHAR(255)
    -- Add other columns based on Field Config.xlsx
);

CREATE TABLE leads (
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

-- Remaining tables: valuation, hoa, rehab, taxes
ETL Script – scripts/etl_load_data.py
Approach:

Load JSON file (fake_property_data_new.json).

Truncate existing tables for clean load.

Create missing columns dynamically using sample JSON.

Insert main property attributes into property.

Insert nested arrays (valuation, HOA, rehab, taxes, leads) into separate tables.

Commit data per property.

Running the ETL:

bash
Copy code
# Activate virtual environment
source venv/Scripts/activate   # Windows
# OR
source venv/bin/activate       # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run ETL
python scripts/etl_load_data.py
Dependencies:

mysql-connector-python

pandas

Data Validation Script – scripts/validate_data.py
Purpose: Cross-check JSON vs MySQL tables to detect missing or mismatched records.

Usage:

bash
Copy code
python scripts/validate_data.py
Behavior:

Reads JSON file.

Checks each property in MySQL tables.

Prints missing or mismatched records for review.

Instructions to Run & Test
Ensure MySQL server is running and database (home_db) exists.

Run sql/create_tables.sql manually or rely on ETL to create tables dynamically.

Place JSON file in data/.

Activate virtual environment.

Install Python dependencies using requirements.txt.

Run etl_load_data.py to load data.

Optionally, run validate_data.py to verify JSON vs database.

Use MySQL queries to check counts:

sql
Copy code
SELECT COUNT(*) FROM property;
SELECT COUNT(*) FROM valuation;
SELECT COUNT(*) FROM hoa;
SELECT COUNT(*) FROM rehab;
SELECT COUNT(*) FROM taxes;
SELECT COUNT(*) FROM leads;
ETL Logic Summary
Dynamic table creation: ensures schema adapts to new fields.

Truncate + load: avoids duplicate records.

Normalization: separates property-related entities into their own tables.

Referential integrity: all nested tables reference property_id.

Validation: cross-verification script ensures JSON load matches MySQL.