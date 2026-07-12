# Example: Snowflake

## What this gives you
- `soda_configuration.yml` and `snowflake_pipeline.py` — a worked example
  gating a Snowflake load by running the Soda CLI, reusing the exact checks
  defined in `soda/checks/customers_checks.yml`
- `dbt/profiles.yml` — connection config for running the dbt tests from the
  top-level `dbt/` folder against Snowflake
- `ge_checkpoint_snowflake.py` — a worked Great Expectations checkpoint using
  the SQL execution engine

**Important:** this is illustrative, not a deployable pipeline as-is. It
assumes data has already landed in Snowflake via a separate load step, and
that each tool is installed wherever its script runs.

## How Soda connects here
Snowflake is a warehouse, not a Spark runtime, so there's no Spark session to
attach to — unlike the Glue and Databricks examples. This goes back to the
same connection method used in `soda/audits/configuration.yml` — a data
source config with credentials — using Snowflake's specific connection fields
(`account`, `warehouse`, `role`) instead of the generic Postgres example
shown there.

## dbt on this platform
- `dbt/profiles.yml` — connection details only, via the `dbt-snowflake`
  adapter — the most natural fit of the three platforms for dbt, since dbt
  compiles to standard SQL Snowflake already understands
- The actual checks live once, platform-agnostically, in this repo's top-level
  `dbt/models/` and `dbt/tests/generic/` folders — they are **not** duplicated
  here

To run:
1. Place `dbt/profiles.yml` at the client's dbt profiles location
2. Copy `dbt/models/` and `dbt/tests/generic/` from this repo's top-level
   `dbt/` folder into the client's actual dbt project
3. Run `dbt test --select stg_customers`

## Great Expectations on this platform
`ge_checkpoint_snowflake.py` connects via GE's SQL execution engine, not the
Spark engine used in the Glue and Databricks examples — same warehouse
connection reasoning as `soda_configuration.yml` above. References the same
`customers_suite` defined once in
`great_expectations/expectations/customers_suite.json`.

## Setup
1. Set the required environment variables (`SODA_SNOWFLAKE_*`,
   `DBT_SNOWFLAKE_*`, `GE_SNOWFLAKE_*`) — never hardcode these into any
   config file in this folder
2. Adapt the load step placeholder in `snowflake_pipeline.py` to the client's
   actual load mechanism (a `COPY INTO`, Snowpipe, or preceding dbt run)
3. Follow the dbt and Great Expectations setup steps above for those tools

## Gating behaviour
`snowflake_pipeline.py` uses the Soda CLI's exit code directly — `0` means all
checks passed, non-zero means at least one failed, mirroring the same
convention dbt uses. Decide per check whether it should be a hard gate or a
soft gate using the relevant pattern doc under `patterns/`.

## Mapping to the pattern library
Same four patterns across all three tools — see `soda/README.md`,
`dbt/README.md`, and `great_expectations/README.md` for the full mapping
tables.

## Known limitations
- Illustrative only — no synthetic dataset included yet
- The load step in `snowflake_pipeline.py` is a placeholder; this example
  focuses on the DQ gate, not the load mechanism itself
- Assumes the Soda CLI, dbt-snowflake adapter, and GE Snowflake dependencies
  are already installed wherever these scripts run