import mysql.connector
import json

# MySQL connection config
config = {
    'host': 'localhost',
    'user': 'db_user',
    'password': '6equj5_db_user',
    'database': 'home_db'
}

# Field mapping for validation
field_mapping = {
    'property': ['property_title', 'address', 'market', 'flood', 'city', 'state', 'zip', 'property_type'],
    'leads': ['reviewed_status', 'most_recent_status', 'source', 'occupancy', 'net_yield', 'irr'],
    'valuation': ['list_price', 'previous_rent', 'zestimate', 'arv', 'expected_rent'],
    'hoa': ['hoa', 'hoa_flag'],
    'rehab': ['underwriting_rehab', 'rehab_calculation', 'paint', 'flooring_flag'],
    'taxes': ['taxes']
}

def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def get_table_property_ids(cursor, table):
    cursor.execute(f"SELECT DISTINCT property_id FROM {table}")
    return set(row['property_id'] for row in cursor.fetchall())

def validate_counts(json_data, cursor, table):
    json_ids = set(record.get('property_id') for record in json_data)
    db_ids = get_table_property_ids(cursor, table)

    missing_in_db = json_ids - db_ids
    extra_in_db = db_ids - json_ids

    return len(json_ids), len(db_ids), missing_in_db, extra_in_db

def validate_sample_fields(json_data, cursor, table, fields, sample_size=5):
    json_dict = {r['property_id']: r for r in json_data if 'property_id' in r}
    cursor.execute(f"SELECT * FROM {table} LIMIT {sample_size}")
    db_rows = cursor.fetchall()
    mismatches = []

    for row in db_rows:
        pid = row['property_id']
        if pid in json_dict:
            json_record = json_dict[pid]
            for f in fields:
                json_val = json_record.get(f)
                db_val = row.get(f)
                if json_val != db_val:
                    mismatches.append({
                        'property_id': pid,
                        'field': f,
                        'json': json_val,
                        'db': db_val
                    })
    return mismatches

def main():
    json_file = '../data/fake_property_data_new.json'
    json_data = load_json(json_file)

    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)

    report_lines = []
    report_lines.append("DATA VALIDATION REPORT\n")
    report_lines.append("======================\n\n")

    for table, fields in field_mapping.items():
        report_lines.append(f"--- Table: {table} ---\n")
        json_count, db_count, missing, extra = validate_counts(json_data, cursor, table)
        report_lines.append(f"JSON records: {json_count}, DB records: {db_count}\n")
        report_lines.append(f"Missing property_ids in DB: {list(missing)[:10]}\n")
        report_lines.append(f"Extra property_ids in DB: {list(extra)[:10]}\n")

        mismatches = validate_sample_fields(json_data, cursor, table, fields)
        report_lines.append(f"Sample field mismatches (max 10):\n")
        for m in mismatches[:10]:
            report_lines.append(f"Property ID {m['property_id']} - Field '{m['field']}': JSON={m['json']} DB={m['db']}\n")

        report_lines.append("\n")

    with open('validation_report.txt', 'w') as f:
        f.writelines(report_lines)

    print("Validation complete. Check 'validation_report.txt' for summary.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
