# How-to: Setting Up CI for DQ Tests

Use this once checks exist and you want them to run automatically on every
pull request, rather than relying on someone remembering to run them by hand.

This uses GitHub Actions, since that's what `.github/workflows/` in this repo
is structured for — the same approach applies with minor syntax differences
for other CI systems (GitLab CI, Azure Pipelines) if the client uses those
instead.

## The core idea
A GitHub Actions workflow is a YAML file that says: "when X happens, run Y."
For DQ, X is usually "a pull request touches a models/checks folder," and Y is
"run the test suite and report pass/fail directly on the PR."

## dbt: `.github/workflows/dbt-test.yml`
```yaml
name: dbt test

on:
  pull_request:
    paths:
      - 'dbt/**'

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dbt
        run: pip install dbt-core dbt-snowflake  # swap adapter per client platform

      - name: Run dbt tests
        working-directory: ./dbt
        env:
          DBT_SNOWFLAKE_ACCOUNT: ${{ secrets.DBT_SNOWFLAKE_ACCOUNT }}
          DBT_SNOWFLAKE_USER: ${{ secrets.DBT_SNOWFLAKE_USER }}
          DBT_SNOWFLAKE_PASSWORD: ${{ secrets.DBT_SNOWFLAKE_PASSWORD }}
        run: dbt test
```

**New concept:** `secrets.DBT_SNOWFLAKE_PASSWORD` pulls from GitHub's own
encrypted secrets store (Settings → Secrets and variables → Actions in the
client's repo), not from a `.env` file — this is the CI-equivalent of the
environment variable habit we've used everywhere else in this repo. Never put
a real credential directly in a workflow file.

## Soda: `.github/workflows/soda-scan.yml`
```yaml
name: soda scan

on:
  pull_request:
    paths:
      - 'soda/**'

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Soda
        run: pip install soda-core-snowflake  # swap package per client platform

      - name: Run Soda scan
        env:
          SODA_DB_USERNAME: ${{ secrets.SODA_DB_USERNAME }}
          SODA_DB_PASSWORD: ${{ secrets.SODA_DB_PASSWORD }}
        run: soda scan -d customers_source -c soda/audits/configuration.yml soda/checks/customers_checks.yml
```

## Great Expectations: `.github/workflows/ge-checkpoint.yml`
```yaml
name: great expectations checkpoint

on:
  pull_request:
    paths:
      - 'great_expectations/**'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install Great Expectations
        run: pip install great_expectations

      - name: Run checkpoint
        env:
          GE_SNOWFLAKE_USER: ${{ secrets.GE_SNOWFLAKE_USER }}
          GE_SNOWFLAKE_PASSWORD: ${{ secrets.GE_SNOWFLAKE_PASSWORD }}
        run: great_expectations checkpoint run customers_checkpoint
```

## A few habits worth keeping across all three
- **`paths:` filters matter** — without them, every PR (even ones that don't
  touch DQ code) triggers a full scan, which slows down unrelated PRs and
  wastes compute. Scope the trigger to the relevant folder.
- **A failing check should fail the PR.** Each of these tools already exits
  non-zero on failure (we covered this in the dbt/Soda/GE READMEs) — GitHub
  Actions automatically marks the job (and the PR check) as failed when a step
  exits non-zero, no extra config needed.
- **Don't run against production data in CI.** Point the CI workflow's
  credentials at a dev/staging environment, not the client's live production
  warehouse — running scans against prod on every PR is both slow and risky.