# How-to: Scaling Checks Across Many Tables

Every example in this repo checks one table (`customers`). A real client
engagement usually has dozens of tables needing the same handful of checks —
primary key integrity, mandatory fields, and so on. This doc covers how to
avoid hand-writing the same check repeatedly.

## The core idea
Instead of writing "customer_id is unique and not null" once per table,
define the *rule* once and apply it to a list of tables/columns. Each tool
has its own mechanism for this.

## dbt: use a `dbt_project.yml` config default, or a loop in a macro
For simple, universal checks (e.g. every table's primary key should be unique
and not null), set defaults in `dbt_project.yml` rather than repeating YAML
per model:
```yaml
models:
  client_project:
    +tests:
      - unique
      - not_null
```
For anything more targeted, a custom generic test macro (like our
`row_count_reconciliation`) already scales naturally — since it's a template
that takes `model`/`compare_model` as arguments, applying it to a new table is
just adding a new YAML block, not writing new SQL each time. The macro is
already the reusable unit — see `dbt/README.md`.

## Soda: generate checks files programmatically, or use a shared checks block
For a small number of tables, a shared block at the top of a checks file
can apply the same rule pattern to several tables:
```yaml
for each dataset_name in [customers, orders, products]:
  checks for $dataset_name:
    - row_count > 0
    - missing_count(id) = 0
```
For a larger number of tables, or where rules vary meaningfully between
tables, it's often more maintainable to generate the checks YAML from a
central rules definition (e.g. `config-templates/dq_rules_template.yml`) using
a small script, rather than hand-maintaining a growing checks file. Worth
treating as a build task on larger engagements rather than assuming SodaCL's
own syntax will scale gracefully past a certain point.

## Great Expectations: loop when building the suite, not in the suite itself
GE expectation suites are just JSON — the templating happens in the Python
code that *builds* the suite, not in the suite format itself:
```python
tables_and_keys = {
    "customers": "customer_id",
    "orders": "order_id",
    "products": "product_id",
}

for table, key_column in tables_and_keys.items():
    suite = context.add_or_update_expectation_suite(f"{table}_suite")
    suite.add_expectation(
        expectation_configuration=gx.expectations.ExpectColumnValuesToNotBeNull(
            column=key_column
        )
    )
    suite.add_expectation(
        expectation_configuration=gx.expectations.ExpectColumnValuesToBeUnique(
            column=key_column
        )
    )
```
This is the same primary key integrity pattern applied across three tables
without three copy-pasted suite files.

## A general principle, regardless of tool
As the number of tables grows, resist writing checks table-by-table from
scratch. Instead:
1. Start from `config-templates/dq_rules_template.yml` as the single source
   of truth for which rule applies to which table/column
2. Generate or template the tool-specific check definitions from that central
   list, rather than maintaining them independently
3. When a rule changes, change it once in the central list — not once per
   table across three tools

This is also why every check in this repo traces back to a pattern doc: at
scale, the pattern is the reusable unit of thought, and the tool-specific
syntax becomes closer to a compilation target than something anyone hand-writes
repeatedly.

## Known limitations
- None of the tool-specific looping shown above is wired up as a working
  script in this repo yet — this doc explains the approach, not a ready-made
  generator. Worth considering as a genuine build task (perhaps living in a
  new `scripts/` folder) once a client engagement has enough tables to justify
  the investment