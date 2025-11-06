# Data Engineering Assessment

Welcome!  
This exercise evaluates your core **data-engineering** skills:

| Competency | Focus                                                         |
| ---------- | ------------------------------------------------------------- |
| SQL        | relational modelling, normalisation, DDL/DML scripting        |
| Python ETL | data ingestion, cleaning, transformation, & loading (ELT/ETL) |

---

## 0 Prerequisites & Setup

> **Allowed technologies**

- **Python ≥ 3.8** – all ETL / data-processing code
- **MySQL 8** – the target relational database
- **Lightweight helper libraries only** (e.g. `pandas`, `mysql-connector-python`).  
  List every dependency in **`requirements.txt`** and justify anything unusual.
- **No ORMs / auto-migration tools** – write plain SQL by hand.

---

## 1 Clone the skeleton repo

```
git clone https://github.com/100x-Home-LLC/data_engineer_assessment.git
```

 Note: Rename the repo after cloning and add your full name.

**Start the MySQL database in Docker:**

```
docker-compose -f docker-compose.initial.yml up --build -d
```

- Database is available on `localhost:3306`
- Credentials/configuration are in the Docker Compose file
- **Do not change** database name or credentials

For MySQL Docker image reference:
[MySQL Docker Hub](https://hub.docker.com/_/mysql)

---

### Problem

- You are provided with a raw JSON file containing property records is located in data/
- Each row relates to a property. Each row mixes many unrelated attributes (property details, HOA data, rehab estimates, valuations, etc.).
- There are multiple Columns related to this property.
- The database is not normalized and lacks relational structure.
- Use the supplied Field Config.xlsx (in data/) to understand business semantics.

### Task

- **Normalize the data:**

  - Develop a Python ETL script to read, clean, transform, and load data into your normalized MySQL tables.
  - Refer the field config document for the relation of business logic
  - Use primary keys and foreign keys to properly capture relationships

- **Deliverable:**
  - Write necessary python and sql scripts
  - Place your scripts in `sql/` and `scripts/`
  - The scripts should take the initial json to your final, normalized schema when executed
  - Clearly document how to run your script, dependencies, and how it integrates with your database.

**Tech Stack:**

- Python (include a `requirements.txt`)
  Use **MySQL** and SQL for all database work
- You may use any CLI or GUI for development, but the final changes must be submitted as python/ SQL scripts
- **Do not** use ORM migrations—write all SQL by hand

---

## Submission Guidelines

- Edit the section to the bottom of this README with your solutions and instructions for each section at the bottom.
- Place all scripts/code in their respective folders (`sql/`, `scripts/`, etc.)
- Ensure all steps are fully **reproducible** using your documentation
- Create a new private repo and invite the reviewer https://github.com/mantreshjain

---

**Good luck! We look forward to your submission.**

## Solutions and Instructions (Filed by Candidate)

**Database Design and Solution**
1. Schema Overview

This project models property listings and their related attributes (valuation, HOA, rehab, taxes, and leads) extracted from a JSON file.
The schema is normalized to 3NF for efficient querying, minimal redundancy, and strong referential integrity.

2. Entity Relationship Overview
Entity	Description	Relationship
property	Base property information	Primary table
valuation	Property valuation details	1-to-many with property
hoa	HOA (Home Owners Association) information	1-to-many with property
rehab	Rehabilitation or renovation data	1-to-many with property
taxes	Property taxes	1-to-1 with property
leads	Lead and review information	1-to-1 with property
3. SQL Table Definitions

The full table creation script is in:
sql/create_tables.sql

Example core table (property):

CREATE TABLE property (
  property_id INT AUTO_INCREMENT PRIMARY KEY,
  property_title VARCHAR(255),
  address VARCHAR(255),
  market VARCHAR(100),
  flood VARCHAR(50),
  street_address VARCHAR(255),
  city VARCHAR(100),
  state VARCHAR(50),
  zip VARCHAR(20),
  property_type VARCHAR(100),
  year_built INT,
  sqft_total VARCHAR(50),
  bed INT,
  bath INT,
  layout VARCHAR(50),
  neighborhood_rating INT,
  latitude DECIMAL(9,6),
  longitude DECIMAL(9,6),
  taxes DECIMAL(12,2)
);


Child tables (like valuation, hoa, rehab, etc.) have a foreign key column:

FOREIGN KEY (property_id) REFERENCES property(property_id)


This ensures all child data belongs to a valid property.

4. Design Decisions

Normalization: To handle nested arrays in the JSON file, each array (like valuation or rehab) is stored in its own table.

Foreign Keys: Enforce referential integrity across tables.

Consistency: Numeric types are standardized using DECIMAL for financial fields and INT for counts.

Extensibility: ETL dynamically maps JSON fields to table columns, allowing future schema changes.

Instructions to Run the Project (Using VS Code)
Open Project in VS Code

Open VS Code

Go to File → Open Folder...

Select your project folder:

C:\Users\Abroz\data_engineer_assessment_afrin_ahmed

Set Up Virtual Environment (venv)

Open the VS Code Terminal → Ctrl + ~

Run the following:

python -m venv venv


Activate the environment:

venv\Scripts\activate


You’ll see (venv) appear in your terminal — this confirms it’s active.
Install Dependencies

In the same terminal (with (venv) active):

pip install -r requirements.txt


This installs packages like:

mysql-connector-python
pandas
openpyxl

Start MySQL

Make sure MySQL is running locally or through Docker.
Example connection (from the script):

config = {
  'host': 'localhost',
  'user': 'db_user',
  'password': '6equj5_db_user',
  'database': 'home_db'
}


If the database doesn’t exist, create it from your MySQL terminal:

CREATE DATABASE home_db;
USE home_db;
SOURCE sql/create_tables.sql;

Run the ETL Script

In VS Code terminal:

python scripts/etl_load_data.py


What happens:

Reads JSON file (data/fake_property_data_new.json)

Parses and cleans property details

Inserts data into MySQL tables (property, valuation, hoa, etc.)

Logs progress in the terminal

Validate Data Load

After ETL finishes, run the validation script:

python scripts/validate_data.py


This script:

Compares the JSON and SQL data

Counts rows and checks for mismatches

Creates a detailed report:
docs/validation_report.txt

You can open it directly in VS Code.

Push Code to GitHub (from VS Code)

Open the Source Control tab in VS Code (icon on left sidebar).

Stage all changes (+ icon).

Commit with a message:

Initial commit: Property ETL Project


Push changes:

git push -u origin main


Verify your repo:
https://github.com/Afrin8055/Property_ETL_Project

ETL Logic and Design
Extract

Reads fake_property_data_new.json from the data/ folder

Parses property-level and nested list data (valuation, hoa, rehab)

Transform

Normalizes data structures (flat JSON → relational tables)

Converts “Yes”/“No”/“Null” to standardized formats (True, False, or None)

Validates data types before loading

Load

Inserts each property first into the property table

Retrieves the generated property_id

Inserts all related valuation, rehab, hoa, leads, and tax data using that property_id as a foreign key

Commits the transaction

Example Code Snippet
# Insert into property table
cursor.execute("""
    INSERT INTO property (property_title, address, market, city, state, zip)
    VALUES (%s, %s, %s, %s, %s, %s)
""", (p['Property_Title'], p['Address'], p['Market'], p['City'], p['State'], p['Zip']))

property_id = cursor.lastrowid

# Insert valuation records
for val in p.get('Valuation', []):
    cursor.execute("""
        INSERT INTO valuation (property_id, list_price, expected_rent)
        VALUES (%s, %s, %s)
    """, (property_id, val['List_Price'], val['Expected_Rent']))

Validation Checks

Run:

python scripts/validate_data.py


This script performs:

Count checks (JSON vs MySQL)

Property presence checks

Mismatch reporting (any missing or extra records)

Writes a text summary in:
📄 docs/validation_report.txt

Requirements

Python 3.8+

MySQL 8

Git

VS Code

Libraries:

mysql-connector-python
pandas
openpyxl

Reviewer Setup Instructions

To reproduce results:

git clone https://github.com/Afrin8055/Property_ETL_Project.git
cd Property_ETL_Project
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python scripts/etl_load_data.py
python scripts/validate_data.py


Then check the validation output in:

docs/validation_report.txt