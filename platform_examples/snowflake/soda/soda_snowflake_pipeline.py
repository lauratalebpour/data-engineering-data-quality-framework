"""
Example pipeline gating a Snowflake load with Soda.
Reuses the exact checks defined in soda/checks/customers_checks.yml -
connects via the warehouse-connection method (see soda_configuration.yml),
not the Spark-session method used in examples/aws_glue and examples/databricks.

This is illustrative - adapt table names and the load step to the client's
actual pipeline (this could equally be triggered from a Snowflake Task, an
external orchestrator, or a CI/CD step after a dbt run against Snowflake).
"""

import subprocess
import sys

# --- Extract / Load --------------------------------------------------------
# In a real pipeline this step already exists - e.g. a COPY INTO statement,
# a Snowpipe, or a preceding dbt run. Shown here as a placeholder for context.
#
#   COPY INTO raw.customers FROM @client_stage/customers/ FILE_FORMAT = (TYPE = CSV);

# --- Data Quality gate ---------------------------------------------------
# Runs the Soda CLI against Snowflake using the warehouse connection config,
# the same pattern shown in soda/README.md, just pointed at this example's
# Snowflake-specific configuration file.
result = subprocess.run(
    [
        "soda", "scan",
        "-d", "customers_source",
        "-c", "examples/snowflake/soda_configuration.yml",
        "soda/checks/customers_checks.yml",
    ],
    capture_output=True,
    text=True,
)

print(result.stdout)

# --- Gate the pipeline on the result -------------------------------------
if result.returncode != 0:
    # Soda's CLI exit code mirrors dbt's convention - non-zero means at least
    # one check failed. A real implementation decides per-check whether this
    # should stop the pipeline (hard gate) or just alert (soft gate) - see
    # patterns/ for guidance.
    print("Data quality checks failed - see scan output above")
    sys.exit(1)

# --- Downstream step would continue here (e.g. promote to a curated schema) --