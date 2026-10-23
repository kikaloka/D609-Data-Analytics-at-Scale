"""Create saved Athena executions for the required screenshot evidence."""
import json
from pathlib import Path
import time
import boto3

athena=boto3.client('athena',region_name='us-east-1')
bucket='d609-stedi-932469575102-20261023'
queries={
 'customer_landing': 'SELECT * FROM stedi.customer_landing ORDER BY email LIMIT 10',
 'accelerometer_landing': 'SELECT * FROM stedi.accelerometer_landing ORDER BY timestamp LIMIT 10',
 'step_trainer_landing': 'SELECT * FROM stedi.step_trainer_landing ORDER BY sensorreadingtime LIMIT 10',
 'customer_landing_missing_consent': 'SELECT email, serialnumber, sharewithresearchasofdate FROM stedi.customer_landing WHERE sharewithresearchasofdate IS NULL LIMIT 10',
 'customer_trusted': 'SELECT email, serialnumber, sharewithresearchasofdate FROM stedi.customer_trusted ORDER BY email LIMIT 10',
 'all_table_counts': " UNION ALL ".join(f"SELECT '{name}' AS table_name, COUNT(*) AS actual_rows FROM stedi.{name}" for name in ['customer_landing','accelerometer_landing','step_trainer_landing','customer_trusted','accelerometer_trusted','customers_curated','step_trainer_trusted','machine_learning_curated'])
}
result={}
for name,sql in queries.items():
    qid=athena.start_query_execution(QueryString=sql,ResultConfiguration={'OutputLocation':f's3://{bucket}/athena/'})['QueryExecutionId']
    while True:
        execution=athena.get_query_execution(QueryExecutionId=qid)['QueryExecution']
        state=execution['Status']['State']
        if state not in ('RUNNING','QUEUED'): break
        time.sleep(1)
    if state!='SUCCEEDED': raise RuntimeError(execution['Status'])
    result[name]={'query_id':qid,'sql':sql,'state':state}
    print('EVIDENCE_QUERY',name,qid,flush=True)
Path('evidence/screenshot-query-ids.json').write_text(json.dumps(result,indent=2))
