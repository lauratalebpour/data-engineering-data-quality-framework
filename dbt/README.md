# DQ in dbt

## What this gives you
- An example staging model (`stg_customers.sql`) showing DQ checks applied via YAML
- Built-in dbt tests (`unique`, `not_null`, `accepted_values`) wired to real patterns
  from `patterns/`
- A custom generic test (`row_count_reconciliation`) implementing
  `patterns/completeness/row-count-reconciliation.md` for cases the built-in tests
  can't cover

**Important:** these files are templates, not a runnable project. They're meant to
be copied into an existing client dbt project — this repo does not connect to a
warehouse and `dbt test` will not run successfully from inside it as-is.

## Setup
1. Copy `models/stg_customers.sql` and `stg_customers.yml` into the client project's
   `models/` folder, adapting field names and logic to the client's actual source table
2. Copy `tests/generic/test_row_count_reconciliation.sql` into the client project's
   `tests/generic/` folder
3. Ensure the client project has a `sources.yml` declaring any source referenced in
   these files (e.g. `raw.customers`) — see "Sources" below
4. Run `dbt test --select stg_customers` to confirm the tests execute

## Sources
Any test using `source('raw', 'customers')` requires that source to be declared
somewhere in the client project, e.g.:

```yaml
version: 2

sources:
  - name: raw
    schema: raw
    tables:
      - name: customers
```

Without this, dbt will throw a compilation error rather than a test failure —
that's a project configuration issue, not a data quality issue.

## Using the built-in tests
Built-in tests (`unique`, `not_null`, `accepted_values`, `relationships`) require
no custom SQL — just add them under a column in the model's YAML file. See
`stg_customers.yml` for examples of all three.

## Using the custom test
```yaml
tests:
  - row_count_reconciliation:
      compare_model: "{{ source('raw', 'customers') }}"
      tolerance_pct: 0
```
- `compare_model`: the table this model's row count should be reconciled against
- `tolerance_pct`: allowed variance as a percentage (0 = exact match required)

## Mapping to the pattern library
Every test here traces back to a pattern doc. When adding a new check for a client,
add it here **and** note which pattern it implements (or write a new pattern doc if
none exists yet):

| Test | Pattern |
|---|---|
| `unique`, `not_null` on `customer_id` | `patterns/uniqueness/primary-key-integrity-check.md` |
| `not_null` on `email` | `patterns/completeness/null-mandatory-field-check.md` |
| `accepted_values` on `country_code` | `patterns/accuracy/reference-data-validation.md` |
| `row_count_reconciliation` | `patterns/completeness/row-count-reconciliation.md` |

## Known limitations
- These tests run at query time against the whole table (or filtered subset) —
  large tables may need sampling or incremental testing strategies not covered here
- The custom test compares raw counts only; it does not check *content* — pair
  with content-level checks for higher-stakes reconciliation work
- No alerting/notification logic is included — test failures surface in `dbt test`
  output and CI logs only, unless wired into the client's existing alerting stack