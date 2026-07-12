"""
Great Expectations checkpoint run against Snowflake directly, using the SQL
execution engine - not the Spark engine used in the Glue and Databricks
examples, since Snowflake is a warehouse with no Spark session to attach to.
Same connection-method split we already saw with Soda.
"""

import great_expectations as gx

context = gx.get_context()

# Connects via a SQL connection string, not a Spark session - credentials
# supplied via environment variables, same habit as every other config in
# this repo.
datasource = context.sources.add_snowflake(
    name="snowflake_source",
    connection_string=(
        "snowflake://${GE_SNOWFLAKE_USER}:${GE_SNOWFLAKE_PASSWORD}"
        "@${GE_SNOWFLAKE_ACCOUNT}/raw/dq_dev"
        "?warehouse=${GE_SNOWFLAKE_WAREHOUSE}&role=${GE_SNOWFLAKE_ROLE}"
    ),
)
data_asset = datasource.add_table_asset(name="customers", table_name="customers")
batch_request = data_asset.build_batch_request()

checkpoint = context.add_or_update_checkpoint(
    name="customers_checkpoint_snowflake",
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