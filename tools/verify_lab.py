"""Run actual Athena validation after all five STEDI Glue jobs succeed."""
import json
from pathlib import Path
import time
import boto3

session = boto3.Session(region_name='us-east-1')
account = session.client('sts').get_caller_identity()['Account']
if account != '932469575102':
    raise RuntimeError('Expected D609 course account')
athena = session.client('athena')
bucket = f'd609-stedi-{account}-20261023'
expected = {'customer_landing':956,'accelerometer_landing':81273,
    'step_trainer_landing':28680,'customer_trusted':482,
    'accelerometer_trusted':40981,'customers_curated':482,
    'step_trainer_trusted':14460,'machine_learning_curated':43681}
queries = {}
for name,count in expected.items():
    queries[name] = (f'SELECT COUNT(*) AS actual_rows FROM stedi.{name}', count)
queries.update({
    'missing_consent_in_trusted': ('SELECT COUNT(*) FROM stedi.customer_trusted WHERE sharewithresearchasofdate IS NULL',0),
    'orphan_accelerometer': ('SELECT COUNT(*) FROM stedi.accelerometer_trusted a WHERE NOT EXISTS (SELECT 1 FROM stedi.customer_trusted c WHERE c.email=a.user)',0),
    'duplicate_curated_customers': ('SELECT COUNT(*) FROM (SELECT email FROM stedi.customers_curated GROUP BY email HAVING COUNT(*)>1)',0),
    'mismatched_training_timestamps': ('SELECT COUNT(*) FROM stedi.machine_learning_curated WHERE sensorreadingtime <> timestamp',0),
    'unconsented_training_users': ('SELECT COUNT(*) FROM stedi.machine_learning_curated m WHERE NOT EXISTS (SELECT 1 FROM stedi.customer_trusted c WHERE c.email=m.user)',0),
    'customer_landing_missing_consent': ('SELECT COUNT(*) FROM stedi.customer_landing WHERE sharewithresearchasofdate IS NULL',474),
})
report = {}
for name,(sql,count) in queries.items():
    qid=athena.start_query_execution(QueryString=sql,ResultConfiguration={'OutputLocation':f's3://{bucket}/athena/'})['QueryExecutionId']
    while True:
        execution=athena.get_query_execution(QueryExecutionId=qid)['QueryExecution']
        state=execution['Status']['State']
        if state not in ('RUNNING','QUEUED'): break
        time.sleep(2)
    if state != 'SUCCEEDED':
        raise RuntimeError(execution['Status'])
    rows=athena.get_query_results(QueryExecutionId=qid)['ResultSet']['Rows']
    actual=int(rows[1]['Data'][0]['VarCharValue'])
    report[name]={'query_id':qid,'query':sql,'actual':actual,'expected':count,
        'passed':actual==count,'bytes_scanned':execution['Statistics'].get('DataScannedInBytes')}
    Path('evidence/athena-validation.json').write_text(json.dumps(report,indent=2))
    print('ATHENA_CHECK',name,actual,'expected',count,'query',qid,flush=True)
    if actual != count:
        raise AssertionError(report[name])
print('ALL_ATHENA_CHECKS_PASSED',flush=True)
