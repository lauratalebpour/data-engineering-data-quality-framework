# DQ in Great Expectations

## What this gives you
- An expectation suite (`customers_suite.json`) implementing the same three
  column-level patterns as the dbt and Soda examples
- A checkpoint (`customers_checkpoint.yml`) showing how a suite gets tied to an
  actual data source and executed
- A custom Python expectation (`expect_row_count_to_reconcile.py`) implementing
  row count reconciliation — the same pattern that needed custom logic in both
  dbt and Soda

**Important:** these files are templates, not a runnable project. They assume an
existing Great Expectations Data Context with a configured data source — this
repo does not connect to a warehouse, and `great_expectations checkpoint run`
will not run successfully from inside it as-is.

## Setup
1. Copy `expectations/customers_suite.json` into the client project's
   `expectations/` folder, adapting column names and value sets to the client's
   actual schema
2. Copy `checkpoints/customers_checkpoint.yml` into the client project's
   `checkpoints/` folder, updating `datasource_name` and `data_asset_name` to
   match the client's configured Data Source (defined separately in
   `great_expectations.yml`)
3. Copy `plugins/expect_row_count_to_reconcile.py` into the client project's
   `plugins/` folder so the custom expectation is discoverable
4. Run the checkpoint to confirm it executes:
```bash
   great_expectations checkpoint run customers_checkpoint
```

## Suites vs checkpoints
Unlike dbt (checks live next to the model) and Soda (checks and connection live
in adjacent YAML files), GE separates **what to check** from **when/where to run
it**:
- An **expectation suite** defines checks once, independent of any environment
- A **checkpoint** runs a suite against a specific data source — the same suite
  can be reused across dev, staging, and prod checkpoints without rewriting checks

## Using the custom expectation
```python
validator.expect_row_count_to_reconcile(
    reference_table_row_count=source_count,
    tolerance_pct=0
)
```
This is a simplified illustrative version. Before using in a real client project,
extend it fully per GE's custom expectation documentation — production use needs
more complete class structure than shown here.

## Data Docs
GE can auto-generate a browsable HTML report of every validation run via the
`UpdateDataDocsAction` in the checkpoint's action list. This is a genuinely useful
thing to offer client stakeholders who want a readable audit trail without
reading YAML or logs — neither dbt nor Soda provide this out of the box.

## Mapping to the pattern library
| Expectation | Pattern |
|---|---|
| `expect_column_values_to_not_be_null`, `expect_column_values_to_be_unique` on `customer_id` | `patterns/uniqueness/primary-key-integrity-check.md` |
| `expect_column_values_to_not_be_null` on `email` | `patterns/completeness/null-mandatory-field-check.md` |
| `expect_column_values_to_be_in_set` on `country_code` | `patterns/accuracy/reference-data-validation.md` |
| `expect_row_count_to_reconcile` (custom) | `patterns/completeness/row-count-reconciliation.md` |

## Known limitations
- Custom expectations require real Python class implementation — more powerful
  for complex logic than dbt or Soda, but a steeper learning curve for simple cases
- The custom expectation included here is illustrative, not production-complete
- No alerting/notification logic is included — checkpoint results surface via
  Data Docs and the checkpoint's action list only, unless wired into the client's
  existing alerting stack