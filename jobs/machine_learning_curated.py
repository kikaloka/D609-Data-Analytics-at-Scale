import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality
from awsglue import DynamicFrame

def sparkSqlQuery(glueContext, query, mapping, transformation_ctx) -> DynamicFrame:
    for alias, frame in mapping.items():
        frame.toDF().createOrReplaceTempView(alias)
    result = spark.sql(query)
    return DynamicFrame.fromDF(result, glueContext, transformation_ctx)
args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Trusted device readings
Trusteddevicereadings_node1793040960753 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="erica_step_trainer_trusted", transformation_ctx="Trusteddevicereadings_node1793040960753")

# Script generated for node Trusted phone readings
Trustedphonereadings_node1793040963720 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="erica_accelerometer_trusted", transformation_ctx="Trustedphonereadings_node1793040963720")

# Script generated for node Paired sensor readings
SqlQuery0 = '''
SELECT
    s.serialnumber,
    s.sensorreadingtime,
    s.distancefromobject,
    a.`user`,
    a.timestamp,
    a.x,
    a.y,
    a.z
FROM s
INNER JOIN a
    ON s.sensorreadingtime = a.timestamp
'''
Pairedsensorreadings_node1793041055717 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"s":Trusteddevicereadings_node1793040960753, "a":Trustedphonereadings_node1793040963720}, transformation_ctx = "Pairedsensorreadings_node1793041055717")

# Script generated for node Machine-learning curated output
EvaluateDataQuality().process_rows(frame=Pairedsensorreadings_node1793041055717, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1793035245951", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
Machinelearningcuratedoutput_node1793041166152 = glueContext.getSink(path="s3://d609-stedi-932469575102-20261023/erica-visual/run-01/machine_learning_curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="Machinelearningcuratedoutput_node1793041166152")
Machinelearningcuratedoutput_node1793041166152.setCatalogInfo(catalogDatabase="stedi",catalogTableName="erica_machine_learning_curated")
Machinelearningcuratedoutput_node1793041166152.setFormat("glueparquet", compression="snappy")
Machinelearningcuratedoutput_node1793041166152.writeFrame(Pairedsensorreadings_node1793041055717)
job.commit()