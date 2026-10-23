"""STEDI machine_learning_curated: reviewed learning-project implementation.

Assistance: OpenAI Codex helped develop, debug, and document this script.
Reads cataloged S3 data, applies the rubric transformation, and creates or
updates its output Data Catalog table. Output is run-specific: no deletes.
"""
import sys
from awsglue.context import GlueContext
from awsglue.dynamicframe import DynamicFrame
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext

args = getResolvedOptions(sys.argv, ['JOB_NAME', 'DATABASE', 'OUTPUT_ROOT'])
glue = GlueContext(SparkContext.getOrCreate())
spark = glue.spark_session
job = Job(glue)
job.init(args['JOB_NAME'], args)

# Read via the catalog to avoid incomplete S3 preview samples.
sources = {'step_trainer_trusted': 's', 'accelerometer_trusted': 'a'}
for table, alias in sources.items():
    frame = glue.create_dynamic_frame.from_catalog(
        database=args['DATABASE'], table_name=table, transformation_ctx=alias)
    frame.toDF().createOrReplaceTempView(alias)

result = spark.sql('SELECT s.sensorreadingtime, s.serialnumber, s.distancefromobject, a.timestamp, a.user, a.x, a.y, a.z FROM s INNER JOIN a ON s.sensorreadingtime = a.timestamp')
actual = result.count()
expected = 43681
if actual != expected:
    raise ValueError('Unexpected machine_learning_curated count: %s; expected %s' % (actual, expected))

sink = glue.getSink(
    connection_type='s3',
    path=args['OUTPUT_ROOT'].rstrip('/') + '/machine_learning_curated/',
    enableUpdateCatalog=True,
    updateBehavior='UPDATE_IN_DATABASE',
    partitionKeys=[],
    compression='snappy',
    transformation_ctx='sink')
sink.setFormat('glueparquet')
sink.setCatalogInfo(catalogDatabase=args['DATABASE'], catalogTableName='machine_learning_curated')
sink.writeFrame(DynamicFrame.fromDF(result, glue, 'result'))
job.commit()
print('STEDI_VALIDATION machine_learning_curated rows=%s' % actual)
