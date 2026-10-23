"""STEDI accelerometer_trusted: reviewed learning-project implementation.

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
sources = {'accelerometer_landing': 'a', 'customer_trusted': 'c'}
for table, alias in sources.items():
    frame = glue.create_dynamic_frame.from_catalog(
        database=args['DATABASE'], table_name=table, transformation_ctx=alias)
    frame.toDF().createOrReplaceTempView(alias)

result = spark.sql('SELECT a.* FROM a INNER JOIN c ON a.user = c.email')
actual = result.count()
expected = 40981
if actual != expected:
    raise ValueError('Unexpected accelerometer_trusted count: %s; expected %s' % (actual, expected))

sink = glue.getSink(
    connection_type='s3',
    path=args['OUTPUT_ROOT'].rstrip('/') + '/accelerometer_trusted/',
    enableUpdateCatalog=True,
    updateBehavior='UPDATE_IN_DATABASE',
    partitionKeys=[],
    compression='snappy',
    transformation_ctx='sink')
sink.setFormat('glueparquet')
sink.setCatalogInfo(catalogDatabase=args['DATABASE'], catalogTableName='accelerometer_trusted')
sink.writeFrame(DynamicFrame.fromDF(result, glue, 'result'))
job.commit()
print('STEDI_VALIDATION accelerometer_trusted rows=%s' % actual)
