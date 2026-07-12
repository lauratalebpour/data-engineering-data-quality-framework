"""
Example Glue ETL job with Soda as the embedded Data Quality check.
Reuses the exact checks defined in soda/checks/customers_checks.yml -
implements the same four patterns as the dbt/, soda/, and great_expectations/
examples.

This is illustrative - adapt source/target paths to the client's actual S3 layout.
"""

import sys
from awsglue.utils import getResolvedOptions # type: ignore
from awsglue.context import GlueContext # type: ignore
from awsglue.job import Job # type: ignore
from pyspark.context import SparkContext # type: ignore
from soda.scan import Scan # type: ignore

args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# --- Extract -----------------------------------------------------------
customers_df = spark.read.option("header", True).csv(
    "s3://client-bucket/raw/customers/"
)
customers_df.createOrReplaceTempView("customers")

# --- Data Quality gate ---------------------------------------------------
# Runs the same checks file used in soda/checks/customers_checks.yml against
# the Spark DataFrame registered above, using Soda's Spark integration.
scan = Scan()
scan.set_scope("customers_scan")
scan.add_spark_session(spark, data_source_name="customers_source")
scan.add_sodacl_yaml_file("soda/checks/customers_checks.yml")
scan.execute()

# --- Gate the pipeline on the result -------------------------------------
if scan.has_check_fails():
    # A real implementation decides here which failures are hard gates
    # (stop the job) vs soft gates (log and continue) - see patterns/ for
    # which checks should block vs warn per pattern.
    print(scan.get_logs_text())
    raise Exception("Data quality checks failed - see scan logs above")

# --- Load ------------------------------------------------------------------
customers_df.write.mode("overwrite").parquet(
    "s3://client-bucket/curated/customers/"
)

job.commit()