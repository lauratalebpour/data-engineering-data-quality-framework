"""
Great Expectations checkpoint run inside a Glue job, using the Spark
execution engine - same connection shape as Soda's add_spark_session()
in glue_job.py in this folder, GE's equivalent concept just named differently.
"""

import great_expectations as gx # type: ignore

context = gx.get_context()

# Connects GE to the Spark session already running inside the Glue job -
# no separate warehouse credentials needed, same reasoning as the Soda example.
datasource = context.sources.add_spark(name="glue_spark_source")
data_asset = datasource.add_dataframe_asset(name="customers")
batch_request = data_asset.build_batch_request(dataframe=customers_df) # type: ignore

checkpoint = context.add_or_update_checkpoint(
    name="customers_checkpoint_glue",
    validations=[
        {
            "batch_request": batch_request,
            "expectation_suite_name": "customers_suite",
        }
    ],
)

result = checkpoint.run()

if not result["success"]:
    raise Exception("Data quality checks failed - see GE Data Docs for detail")