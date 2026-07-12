# Example: AWS Glue

## What this gives you
- `glue_job.py` — a worked Glue ETL job with Soda embedded as a data quality
  gate, reusing the exact checks defined in `soda/checks/customers_checks.yml`
- `dbt/profiles.yml` — connection config for running the dbt tests from the
  top-level `dbt/` folder against Glue
- `ge_checkpoint_glue.py` — a worked Great Expectations checkpoint using the
  Spark execution engine

**Important:** this is illustrative, not a deployable job as-is. Paths and
table names are placeholders, and each tool assumes its dependencies are
already installed in the target environment.

## How Soda connects here
Glue runs on Spark, so Soda connects directly to the running Spark session via
`scan.add_spark_session()` — no separate warehouse credentials needed, since
the DataFrame itself is the data being checked, before it's landed anywhere.
This differs from `soda/audits/configuration.yml`, which connects to an
already-landed warehouse table. See `soda/README.md` → "Connection methods".

## dbt on this platform
- `dbt/profiles.yml` — connection details only, via the `dbt-glue` adapter
  (Glue interactive sessions/Athena)
- The actual checks live once, platform-agnostically, in this repo's top-level
  `dbt/models/` and `dbt/tests/generic/` folders — they are **not** duplicated
  here

To run:
1. Place `dbt/profiles.yml` at the client's dbt profiles location (usually
   `~/.dbt/profiles.yml`, or wherever `DBT_PROFILES_DIR` points)
2. Copy `dbt/models/` and `dbt/tests/generic/` from this repo's top-level
   `dbt/` folder into the client's actual dbt project
3. Run `dbt test --select stg_customers`

A profile with no project is meaningless, and a project with no profile has
nowhere to run — dbt only works with both present.

## Great Expectations on this platform
`ge_checkpoint_glue.py` connects via GE's Spark execution engine — the same
connection reasoning as Soda's `add_spark_session()` above, just GE's version
of it. It references `expectation_suite_name: "customers_suite"`, the same
suite defined once in `great_expectations/expectations/customers_suite.json`.

## Setup
1. Package the Soda library as a Glue job dependency
   (`--additional-python-modules soda-core-spark-df`), since it's not
   available in Glue by default
2. Adapt the S3 paths in `glue_job.py` to the client's actual raw and curated
   locations
3. Follow the dbt and Great Expectations setup steps above for those tools

## Gating behaviour
`glue_job.py` uses a simple hard gate — any check failure raises an exception,
stopping the job before Load runs. Decide per check whether it should be a
hard gate or a soft gate using the relevant pattern doc under `patterns/`.

## Mapping to the pattern library
Same four patterns across all three tools — see `soda/README.md`,
`dbt/README.md`, and `great_expectations/README.md` for the full mapping
tables.

## Known limitations
- Illustrative only — no synthetic dataset included yet, so nothing here runs
  end to end without a client's actual environment
- Native AWS Glue Data Quality (DQDL) is a separate, AWS-native alternative to
  bringing in these three tools — not yet covered in this example