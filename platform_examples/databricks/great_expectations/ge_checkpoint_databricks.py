"""
Great Expectations checkpoint run inside a Databricks job, using the Spark
execution engine - identical connection shape to examples/aws_glue, since
both platforms run on Spark.
"""

import great_expectations as gx # type: ignore

context = gx.get_context()

datasource = context.sources.add_spark(name="databricks_spark_source")
data_asset = datasource.add_dataframe_asset(name="customers")
batch_request = data_asset.build_batch_request(dataframe=customers_df) # type: ignore

checkpoint = context.add_or_update_checkpoint(
    name="customers_checkpoint_databricks",
    validations=[
        {
            "batch_request": batch_request,
            "expectation_suite_name": "customers_suite",
        }
    ],
)

result = checkpoint.run()

if not result["success"]:
    dbutils.notebook.exit("DQ_CHECK_FAILED") # type: ignore