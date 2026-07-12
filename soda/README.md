# DQ in Soda

## What this gives you
- A checks file (`customers_checks.yml`) implementing the same four patterns as the
  dbt example, so the two tools can be compared side by side
- A data source configuration template (`configuration.yml`) showing safe,
  environment-variable-based credential handling
- A worked example of a user-defined SQL check for cases SodaCL's built-in
  metrics can't cover

**Important:** these files are templates, not a runnable project. They assume a
data source is already connected — this repo does not connect to a warehouse, and
`soda scan` will not run successfully from inside it as-is.

## Setup
1. Copy `checks/customers_checks.yml` into the client project's checks folder,
   adapting table and column names to the client's actual schema
2. Copy `audits/configuration.yml` into the client project's Soda config location,
   updating the `data_source` name, `type` (postgres, snowflake, bigquery, etc.),
   and connection details
3. Set the required environment variables (`SODA_DB_HOST`, `SODA_DB_PORT`,
   `SODA_DB_USERNAME`, `SODA_DB_PASSWORD`, `SODA_DB_NAME`) in the client's
   environment — **never** hardcode these values into the YAML file
4. Run a scan to confirm the checks execute:
```bash
   soda scan -d customers_source -c soda/audits/configuration.yml soda/checks/customers_checks.yml
```

## Using built-in checks
Most common checks (`missing_count`, `duplicate_count`, `invalid_count`,
`freshness`) need no custom SQL — just a line of SodaCL. See
`customers_checks.yml` for examples of all four.

## Connection methods
The `configuration.yml` example in this folder connects Soda to a warehouse via
a data source config (Postgres, Snowflake, BigQuery, etc.). Soda can also connect
directly to a Spark DataFrame at runtime — see `examples/aws_glue/glue_job.py`
for a worked example of that method, used when Soda runs inside a Glue/Spark job
rather than against a standalone warehouse connection.


## Using a user-defined SQL check
For logic built-in metrics can't express (like comparing counts across two
tables), write a named SQL block:
```yaml
checks for customers:
  - row_count_reconciliation:
      row_count_reconciliation query: |
        SELECT
          (SELECT COUNT(*) FROM raw.customers) AS source_count,
          (SELECT COUNT(*) FROM customers) AS target_count
```

## Mapping to the pattern library
| Check | Pattern |
|---|---|
| `missing_count`, `duplicate_count` on `customer_id` | `patterns/uniqueness/primary-key-integrity-check.md` |
| `missing_count` on `email` | `patterns/completeness/null-mandatory-field-check.md` |
| `invalid_count` on `country_code` | `patterns/accuracy/reference-data-validation.md` |
| `freshness` on `created_at` | `patterns/timeliness/freshness-sla-check.md` |
| `row_count_reconciliation` | `patterns/completeness/row-count-reconciliation.md` |

## Known limitations
- User-defined SQL checks (like row count reconciliation) are less elegant in Soda
  than dbt's macro system — there's no reusable "generic test" equivalent, so each
  reconciliation check is written out in full per table
- Credentials must be supplied via environment variables at scan time — this repo
  contains no working connection and cannot be scanned as-is
- No alerting/notification logic is included — scan results surface in the scan
  output only, unless wired into the client's existing alerting stack or Soda Cloud