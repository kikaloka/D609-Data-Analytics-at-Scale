"""STEDI step_trainer_trusted: reviewed learning-project implementation.

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
sources = {'step_trainer_landing': 's', 'customers_curated': 'c'}
for table, alias in sources.items():
    frame = glue.create_dynamic_frame.from_catalog(
        database=args['DATABASE'], table_name=table, transformation_ctx=alias)
    frame.toDF().createOrReplaceTempView(alias)

result = spark.sql('SELECT DISTINCT s.* FROM s INNER JOIN c ON s.serialnumber = c.serialnumber')
actual = result.count()
expected = 14460
if actual != expected:
    raise ValueError('Unexpected step_trainer_trusted count: %s; expected %s' % (actual, expected))

sink = glue.getSink(
    connection_type='s3',
    path=args['OUTPUT_ROOT'].rstrip('/') + '/step_trainer_trusted/',
    enableUpdateCatalog=True,
    updateBehavior='UPDATE_IN_DATABASE',
    partitionKeys=[],
    compression='snappy',
    transformation_ctx='sink')
sink.setFormat('glueparquet')
sink.setCatalogInfo(catalogDatabase=args['DATABASE'], catalogTableName='step_trainer_trusted')
sink.writeFrame(DynamicFrame.fromDF(result, glue, 'result'))
job.commit()
print('STEDI_VALIDATION step_trainer_trusted rows=%s' % actual)
