# Example: Databricks

## What this gives you
- `databricks_job.py` — a worked Databricks job with Soda embedded as a data
  quality gate, reusing the exact checks defined in
  `soda/checks/customers_checks.yml`
- `dbt/profiles.yml` — connection config for running the dbt tests from the
  top-level `dbt/` folder against Databricks
- `ge_checkpoint_databricks.py` — a worked Great Expectations checkpoint using
  the Spark execution engine

**Important:** this is illustrative, not a deployable job as-is. Table names
are placeholders, and each tool assumes its dependencies are already
installed in the target environment.

## How Soda connects here
Databricks runs on Spark, so Soda connects the same way as the Glue example —
directly to the running Spark session via `scan.add_spark_session()`, no
separate warehouse credentials needed. If you've read `examples/aws_glue`
already, this will look nearly identical; the differences are platform-specific
plumbing (Delta table reads, and `dbutils.notebook.exit()` instead of a raised
exception to signal failure to the orchestrator).

## dbt on this platform
- `dbt/profiles.yml` — connection details only, via the `dbt-databricks`
  adapter
- The actual checks live once, platform-agnostically, in this repo's top-level
  `dbt/models/` and `dbt/tests/generic/` folders — they are **not** duplicated
  here

To run:
1. Place `dbt/profiles.yml` at the client's dbt profiles location
2. Copy `dbt/models/` and `dbt/tests/generic/` from this repo's top-level
   `dbt/` folder into the client's actual dbt project
3. Run `dbt test --select stg_customers`

## Great Expectations on this platform
`ge_checkpoint_databricks.py` connects via GE's Spark execution engine — same
connection shape as `examples/aws_glue/ge_checkpoint_glue.py`, since both
platforms run on Spark. References the same `customers_suite` defined once in
`great_expectations/expectations/customers_suite.json`.

## Setup
1. Install Soda as a cluster library (`soda-core-spark-df`) via the Databricks
   cluster configuration
2. Adapt the table names in `databricks_job.py` to the client's actual Unity
   Catalog or Hive metastore layout
3. Follow the dbt and Great Expectations setup steps above for those tools

## Gating behaviour
`databricks_job.py` uses `dbutils.notebook.exit()` on failure — this is how a
Databricks notebook signals failure status to a Databricks Workflow
orchestrating it, distinct from Glue's raised Python exception but achieving
the same outcome: stopping before Load runs. Decide per check whether it
should be a hard gate or a soft gate using the relevant pattern doc under
`patterns/`.

## Mapping to the pattern library
Same four patterns across all three tools — see `soda/README.md`,
`dbt/README.md`, and `great_expectations/README.md` for the full mapping
tables.

## Known limitations
- Illustrative only — no synthetic dataset included yet
- Assumes Unity Catalog or metastore tables already exist; doesn't cover
  initial table creation or Delta Lake setup