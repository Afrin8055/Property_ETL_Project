import json
import mysql.connector

# MySQL connection config
config = {
    'host': 'localhost',
    'user': 'db_user',
    'password': '6equj5_db_user',
    'database': 'home_db'
}

# Tables and nested relationships
nested_tables = ['valuation', 'hoa', 'rehab', 'taxes', 'leads']

def main():
    # Load JSON data
    with open('../data/fake_property_data_new.json', 'r') as f:
        data = json.load(f)

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    print("Connected to MySQL")

    missing = {table: [] for table in nested_tables}

    for record in data:
        property_id = record.get('property_id')

        # Check main property table
        cursor.execute("SELECT COUNT(*) FROM property WHERE property_id=%s", (property_id,))
        if cursor.fetchone()[0] == 0:
            print(f"Property {property_id} missing in property table")
            continue

        # Check nested tables
        for table in nested_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table} WHERE property_id=%s", (property_id,))
            count = cursor.fetchone()[0]
            if count == 0:
                missing[table].append(property_id)

    cursor.close()
    conn.close()
    print("Connection closed.\n")

    # Report missing
    for table, props in missing.items():
        if props:
            print(f"{len(props)} properties missing in {table}: {props[:10]}{'...' if len(props) > 10 else ''}")
        else:
            print(f"All properties present in {table}")

if __name__ == "__main__":
    main()
