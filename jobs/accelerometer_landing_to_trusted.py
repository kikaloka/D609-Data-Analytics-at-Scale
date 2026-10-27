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

# Script generated for node Accelerometer landing
Accelerometerlanding_node1793035366622 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="accelerometer_landing", transformation_ctx="Accelerometerlanding_node1793035366622")

# Script generated for node Eligible customers
Eligiblecustomers_node1793035449443 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="erica_customer_trusted", transformation_ctx="Eligiblecustomers_node1793035449443")

# Script generated for node Eligible movement readings
SqlQuery0 = '''
SELECT a.*
FROM a
INNER JOIN c
    ON a.`user` = c.email
    
'''
Eligiblemovementreadings_node1793035536557 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"a":Accelerometerlanding_node1793035366622, "c":Eligiblecustomers_node1793035449443}, transformation_ctx = "Eligiblemovementreadings_node1793035536557")

# Script generated for node Accelerometer trusted output
EvaluateDataQuality().process_rows(frame=Eligiblemovementreadings_node1793035536557, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1793035245951", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
Accelerometertrustedoutput_node1793036717648 = glueContext.getSink(path="s3://d609-stedi-932469575102-20261023/erica-visual/run-01/accelerometer_trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="Accelerometertrustedoutput_node1793036717648")
Accelerometertrustedoutput_node1793036717648.setCatalogInfo(catalogDatabase="stedi",catalogTableName="erica_accelerometer_trusted")
Accelerometertrustedoutput_node1793036717648.setFormat("glueparquet", compression="snappy")
Accelerometertrustedoutput_node1793036717648.writeFrame(Eligiblemovementreadings_node1793035536557)
job.commit()