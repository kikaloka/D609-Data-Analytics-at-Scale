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

# Script generated for node Customer landing
Customerlanding_node1793034001756 = glueContext.create_dynamic_frame.from_catalog(database="stedi", table_name="customer_landing", transformation_ctx="Customerlanding_node1793034001756")

# Script generated for node Research consent filter
SqlQuery0 = '''
SELECT *
FROM myDataSource
WHERE sharewithresearchasofdate IS NOT NULL
'''
Researchconsentfilter_node1793034324315 = sparkSqlQuery(glueContext, query = SqlQuery0, mapping = {"myDataSource":Customerlanding_node1793034001756}, transformation_ctx = "Researchconsentfilter_node1793034324315")

# Script generated for node Customer trusted output
EvaluateDataQuality().process_rows(frame=Researchconsentfilter_node1793034324315, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1793033693962", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
Customertrustedoutput_node1793034461620 = glueContext.getSink(path="s3://d609-stedi-932469575102-20261023/erica-visual/run-01/customer_trusted/", connection_type="s3", updateBehavior="UPDATE_IN_DATABASE", partitionKeys=[], enableUpdateCatalog=True, transformation_ctx="Customertrustedoutput_node1793034461620")
Customertrustedoutput_node1793034461620.setCatalogInfo(catalogDatabase="stedi",catalogTableName="erica_customer_trusted")
Customertrustedoutput_node1793034461620.setFormat("glueparquet", compression="snappy")
Customertrustedoutput_node1793034461620.writeFrame(Researchconsentfilter_node1793034324315)
job.commit()