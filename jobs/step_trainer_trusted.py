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

# Script generated for node Step-trainer landing
Steptrainerlanding_node1793040226522 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="step_trainer_landing", transformation_ctx="Steptrainerlanding_node1793040226522")

# Script generated for node Curated customers
Curatedcustomers_node1793040232461 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="erica_customers_curated", transformation_ctx="Curatedcustomers_node1793040232461")

# Script generated for node Eligible device readings
SqlQuery0 = '''
SELECT DISTINCT s.*
FROM s
INNER JOIN c
    ON s.serialnumber = c.serialnumber
'''
Eligibledevicereadings_node1793040360032 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"s":Steptrainerlanding_node1793040226522, "c":Curatedcustomers_node1793040232461}, transformation_ctx = "Eligibledevicereadings_node1793040360032")

# Script generated for node Step-trainer trusted output
EvaluateDataQuality().process_rows(frame=Eligibledevicereadings_node1793040360032, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1793035245951", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
Steptrainertrustedoutput_node1793040422676 = glueContext.getSink(path="s3://d609-stedi-932469575102-20261023/erica-visual/run-01/step_trainer_trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="Steptrainertrustedoutput_node1793040422676")
Steptrainertrustedoutput_node1793040422676.setCatalogInfo(catalogDatabase="stedi",catalogTableName="erica_step_trainer_trusted")
Steptrainertrustedoutput_node1793040422676.setFormat("glueparquet", compression="snappy")
Steptrainertrustedoutput_node1793040422676.writeFrame(Eligibledevicereadings_node1793040360032)
job.commit()