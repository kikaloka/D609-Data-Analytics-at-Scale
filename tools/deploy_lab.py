"""Deploy to the temporary course AWS account, using its existing login.

No credentials are embedded. Role creation requires --create-role.
Run from the project root. This creates only new D609-named resources.
"""
import argparse
import io
import json
from pathlib import Path
import time
import urllib.request
import zipfile
import boto3
from botocore.exceptions import ClientError

parser = argparse.ArgumentParser()
parser.add_argument('--create-role', action='store_true')
parser.add_argument('--run', action='store_true')
args = parser.parse_args()
session = boto3.Session(region_name='us-east-1')
account = session.client('sts').get_caller_identity()['Account']
if account != '932469575102':
    raise RuntimeError('Refusing to deploy outside the observed D609 course account')
bucket = f'd609-stedi-{account}-20261023'
database = 'stedi'
role_name = 'D609-STEDI-GlueRole'
s3, glue, iam = [session.client(x) for x in ('s3', 'glue', 'iam')]
try:
    s3.head_bucket(Bucket=bucket)
except ClientError as exc:
    if exc.response['Error']['Code'] not in ('404', 'NoSuchBucket'):
        raise
    s3.create_bucket(Bucket=bucket)
s3.put_public_access_block(Bucket=bucket, PublicAccessBlockConfiguration={
    'BlockPublicAcls':True, 'IgnorePublicAcls':True,
    'BlockPublicPolicy':True, 'RestrictPublicBuckets':True})
s3.put_bucket_encryption(Bucket=bucket, ServerSideEncryptionConfiguration={
    'Rules':[{'ApplyServerSideEncryptionByDefault':{'SSEAlgorithm':'AES256'}}]})

url = 'https://codeload.github.com/udacity/nd027-Data-Engineering-Data-Lakes-AWS-Exercises/zip/refs/heads/main'
archive = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(url).read()))
counts = {}
for name in archive.namelist():
    if '/project/starter/' not in name or not name.endswith('.json'):
        continue
    tail = name.split('/project/starter/',1)[1]
    parts = tail.split('/')
    if len(parts) != 3 or parts[1] != 'landing':
        continue
    data = archive.read(name)
    counts[parts[0]] = counts.get(parts[0], 0) + len([x for x in data.splitlines() if x.strip()])
    s3.put_object(Bucket=bucket,Key=f'landing/{parts[0]}/{parts[2]}',Body=data)
assert counts == {'customer':956,'accelerometer':81273,'step_trainer':28680}, counts
try:
    glue.create_database(DatabaseInput={'Name':database})
except glue.exceptions.AlreadyExistsException:
    pass
profile = json.loads(Path('evidence/local-data-profile.json').read_text())
for name in ('customer','accelerometer','step_trainer'):
    columns=[]
    for key,kinds in profile[name]['fields'].items():
        typ='double' if 'float' in kinds else 'bigint' if 'int' in kinds else 'string'
        columns.append({'Name':key.lower(),'Type':typ})
    table={'Name':name+'_landing','TableType':'EXTERNAL_TABLE',
        'Parameters':{'classification':'json','EXTERNAL':'TRUE'},
        'StorageDescriptor':{'Columns':columns,'Location':f's3://{bucket}/landing/{name}/',
            'InputFormat':'org.apache.hadoop.mapred.TextInputFormat',
            'OutputFormat':'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat',
            'SerdeInfo':{'SerializationLibrary':'org.openx.data.jsonserde.JsonSerDe','Parameters':{'case.insensitive':'true'}}}}
    try:
        glue.create_table(DatabaseName=database,TableInput=table)
    except glue.exceptions.AlreadyExistsException:
        pass
print('LANDING_READY',bucket,counts,flush=True)

trust={'Version':'2012-10-17','Statement':[{'Effect':'Allow',
    'Principal':{'Service':'glue.amazonaws.com'},'Action':'sts:AssumeRole'}]}
policy={'Version':'2012-10-17','Statement':[
    {'Effect':'Allow','Action':['s3:GetBucketLocation','s3:ListBucket'],'Resource':f'arn:aws:s3:::{bucket}'},
    {'Effect':'Allow','Action':['s3:GetObject','s3:PutObject'],'Resource':f'arn:aws:s3:::{bucket}/*'},
    {'Effect':'Allow','Action':['glue:GetDatabase','glue:GetTable','glue:GetTables','glue:GetPartitions','glue:GetPartition','glue:BatchGetPartition','glue:CreateTable','glue:UpdateTable','glue:BatchCreatePartition','glue:CreatePartition','glue:UpdatePartition'],
     'Resource':[f'arn:aws:glue:us-east-1:{account}:catalog',f'arn:aws:glue:us-east-1:{account}:database/stedi',f'arn:aws:glue:us-east-1:{account}:table/stedi/*']},
    {'Effect':'Allow','Action':['logs:CreateLogGroup','logs:CreateLogStream','logs:PutLogEvents'],
     'Resource':f'arn:aws:logs:us-east-1:{account}:log-group:/aws-glue/*'}]}
Path('evidence/proposed-role-trust.json').write_text(json.dumps(trust,indent=2))
Path('evidence/proposed-role-policy.json').write_text(json.dumps(policy,indent=2))
if not args.create_role:
    print('ROLE_APPROVAL_REQUIRED: rerun with --create-role only after approval',flush=True)
    raise SystemExit(0)
try:
    role=iam.create_role(RoleName=role_name,AssumeRolePolicyDocument=json.dumps(trust),Description='D609 course-only Glue ETL access')['Role']
except iam.exceptions.EntityAlreadyExistsException:
    role=iam.get_role(RoleName=role_name)['Role']
iam.put_role_policy(RoleName=role_name,PolicyName='D609-STEDI-ScopedAccess',PolicyDocument=json.dumps(policy))
time.sleep(15)
order=['customer_landing_to_trusted','accelerometer_landing_to_trusted','customer_trusted_to_curated','step_trainer_trusted','machine_learning_curated']
run_root=f's3://{bucket}/runs/{int(time.time())}'
results=[]
for name in order:
    s3.upload_file('jobs/'+name+'.py',bucket,'scripts/'+name+'.py')
    job={'Role':role['Arn'],'Command':{'Name':'glueetl','PythonVersion':'3','ScriptLocation':f's3://{bucket}/scripts/{name}.py'},
        'DefaultArguments':{'--DATABASE':database,'--OUTPUT_ROOT':run_root,'--job-bookmark-option':'job-bookmark-disable','--enable-metrics':'false'},
        'GlueVersion':'4.0','WorkerType':'G.1X','NumberOfWorkers':2,'Timeout':15,'MaxRetries':0}
    try:
        glue.create_job(Name='D609-'+name,**job)
    except glue.exceptions.AlreadyExistsException:
        glue.update_job(JobName='D609-'+name,JobUpdate=job)
    if args.run:
        rid=glue.start_job_run(JobName='D609-'+name)['JobRunId']
        print('JOB_STARTED',name,rid,flush=True)
        while True:
            run=glue.get_job_run(JobName='D609-'+name,RunId=rid)['JobRun']
            state=run['JobRunState']
            if state not in ('STARTING','WAITING','RUNNING','STOPPING'):
                results.append({'job':name,'run_id':rid,'state':state,'error':run.get('ErrorMessage'),'seconds':run.get('ExecutionTime')})
                Path('evidence/aws-job-runs.json').write_text(json.dumps(results,indent=2))
                print('JOB_FINISHED',results[-1],flush=True)
                if state != 'SUCCEEDED':
                    raise RuntimeError('Stopped after unsuccessful job')
                break
            time.sleep(15)
Path('evidence/lab-resources.json').write_text(json.dumps({'account':account,'bucket':bucket,'database':database,'role':role['Arn'],'output_root':run_root},indent=2))
print('DEPLOYMENT_COMPLETE',flush=True)
