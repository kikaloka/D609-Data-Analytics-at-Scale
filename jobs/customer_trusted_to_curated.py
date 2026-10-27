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

# Script generated for node Trusted customers
Trustedcustomers_node1793039334244 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="erica_customer_trusted", transformation_ctx="Trustedcustomers_node1793039334244")

# Script generated for node Trusted movement readings
Trustedmovementreadings_node1793039371208 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="erica_accelerometer_trusted", transformation_ctx="Trustedmovementreadings_node1793039371208")

# Script generated for node Customers with movement data
SqlQuery0 = '''
SELECT DISTINCT c.*
FROM c
INNER JOIN a
    ON c.email = a.`user`
    
'''
Customerswithmovementdata_node1793039546848 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"a":Trustedmovementreadings_node1793039371208, "c":Trustedcustomers_node1793039334244}, transformation_ctx = "Customerswithmovementdata_node1793039546848")

# Script generated for node Customers curated output
EvaluateDataQuality().process_rows(frame=Customerswithmovementdata_node1793039546848, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1793035245951", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
Customerscuratedoutput_node1793039642141 = glueContext.getSink(path="s3://d609-stedi-932469575102-20261023/erica-visual/run-01/customers_curated/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="Customerscuratedoutput_node1793039642141")
Customerscuratedoutput_node1793039642141.setCatalogInfo(catalogDatabase="stedi",catalogTableName="erica_customers_curated")
Customerscuratedoutput_node1793039642141.setFormat("glueparquet", compression="snappy")
Customerscuratedoutput_node1793039642141.writeFrame(Customerswithmovementdata_node1793039546848)
job.commit()