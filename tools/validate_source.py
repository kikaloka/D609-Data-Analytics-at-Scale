import json
import sqlite3
from pathlib import Path

import argparse
parser = argparse.ArgumentParser(description='Local SQL reference validation of official STEDI data')
parser.add_argument('starter_directory', type=Path)
parser.add_argument('--report', type=Path, default=Path('evidence/local-data-profile.json'))
args = parser.parse_args()
root = args.starter_directory
db = sqlite3.connect(':memory:')
report = {}
for folder in ('customer', 'accelerometer', 'step_trainer'):
    records = [json.loads(line) for file in sorted((root / folder / 'landing').glob('*.json')) for line in file.read_text().splitlines() if line.strip()]
    fields = sorted({key for row in records for key in row})
    types = {key: sorted({type(row.get(key)).__name__ for row in records}) for key in fields}
    db.execute(f'CREATE TABLE "{folder}" ({", ".join(chr(34)+key+chr(34) for key in fields)})')
    db.executemany(f'INSERT INTO "{folder}" VALUES ({",".join("?" for _ in fields)})', [[r.get(key) for key in fields] for r in records])
    report[folder] = {'rows': len(records), 'fields': types}
queries = {
    'customer_trusted': 'SELECT * FROM customer WHERE shareWithResearchAsOfDate IS NOT NULL',
    'accelerometer_trusted': 'SELECT a.* FROM accelerometer a JOIN customer_trusted c ON a.user = c.email',
    'customers_curated': 'SELECT DISTINCT c.* FROM customer_trusted c JOIN accelerometer_trusted a ON c.email = a.user',
    'step_trainer_trusted': 'SELECT DISTINCT s.* FROM step_trainer s JOIN customers_curated c ON s.serialNumber = c.serialNumber',
    'machine_learning_curated': 'SELECT s.*, a.* FROM step_trainer_trusted s JOIN accelerometer_trusted a ON s.sensorReadingTime = a.timestamp',
}
for table, sql in queries.items():
    db.execute(f'CREATE TABLE {table} AS {sql}')
    report[table] = {'rows': db.execute(f'SELECT COUNT(*) FROM {table}').fetchone()[0]}
expected = {'customer':956,'accelerometer':81273,'step_trainer':28680,
    'customer_trusted':482,'accelerometer_trusted':40981,'customers_curated':482,
    'step_trainer_trusted':14460,'machine_learning_curated':43681}
for table, count in expected.items():
    assert report[table]['rows'] == count, (table, report[table]['rows'], count)
checks = {
    'trusted_customers_without_consent': 'SELECT COUNT(*) FROM customer_trusted WHERE shareWithResearchAsOfDate IS NULL',
    'trusted_accelerometer_without_consented_customer': 'SELECT COUNT(*) FROM accelerometer_trusted a WHERE NOT EXISTS (SELECT 1 FROM customer_trusted c WHERE c.email=a.user)',
    'duplicate_curated_customer_emails': 'SELECT COUNT(*) FROM (SELECT email FROM customers_curated GROUP BY email HAVING COUNT(*)>1)',
    'duplicate_trusted_step_records': 'SELECT COUNT(*) FROM (SELECT sensorReadingTime,serialNumber,distanceFromObject FROM step_trainer_trusted GROUP BY 1,2,3 HAVING COUNT(*)>1)',
}
report['integrity_checks'] = {name: db.execute(query).fetchone()[0] for name,query in checks.items()}
assert not any(report['integrity_checks'].values()), report['integrity_checks']
print(json.dumps(report, indent=2))
args.report.write_text(json.dumps(report, indent=2))
