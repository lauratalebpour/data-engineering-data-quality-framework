"""
Example Databricks job with Soda as the embedded Data Quality check.
Reuses the exact checks defined in soda/checks/customers_checks.yml -
same pattern as examples/aws_glue/glue_job.py, since both Glue and Databricks
run on Spark and connect Soda via the Spark session method.

This is illustrative - adapt table names to the client's actual Unity Catalog
or Hive metastore layout.
""" 
from soda.scan import Scan # type: ignore

# --- Extract -----------------------------------------------------------
# Reads from a Delta table rather than raw S3/CSV, since Databricks typically
# operates on Delta Lake tables already registered in the catalog.
customers_df = spark.read.table("raw.customers") # type: ignore
customers_df.createOrReplaceTempView("customers")

# --- Data Quality gate ---------------------------------------------------
# Identical connection method to examples/aws_glue/glue_job.py - Soda attaches
# directly to the running Spark session, no separate warehouse credentials needed.
scan = Scan()
scan.set_scope("customers_scan")
scan.add_spark_session(spark, data_source_name="customers_source") # type: ignore
scan.add_sodacl_yaml_file("soda/checks/customers_checks.yml")
scan.execute()

# --- Gate the pipeline on the result -------------------------------------
if scan.has_check_fails():
    print(scan.get_logs_text())
    # dbutils.notebook.exit() with a non-zero-equivalent message is how a
    # Databricks job signals failure to the orchestrating job/workflow -
    # different mechanism to Glue's raised Exception, same intent: stop before Load.
    dbutils.notebook.exit("DQ_CHECK_FAILED") # type: ignore

# --- Load ------------------------------------------------------------------
customers_df.write.mode("overwrite").saveAsTable("curated.customers")