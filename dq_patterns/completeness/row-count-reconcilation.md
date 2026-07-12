# Pattern: Row Count Reconciliation

**Dimension:** Completeness

## The problem
Data moves between systems constantly — source database to warehouse, one pipeline
stage to the next, a vendor feed to an internal table. At any of these hops, rows
can silently go missing (a failed batch, a bad filter, a join that unintentionally
drops records) with no error thrown. Without an explicit check, nobody notices
until a client or stakeholder spots the discrepancy downstream — which is the
worst possible time to find out.

## When to use it
- Any time data crosses a system boundary (source → staging, staging → warehouse,
  internal → external feed)
- Especially important after any full or incremental load, not just full loads
- Use alongside more granular checks (see Reconciliation Checkpoint pattern) when
  row counts alone aren't enough to prove correctness

## How it works
1. Identify the **source** count: count of rows expected, at a defined point in time
   (e.g. count in the source table as of the extract timestamp)
2. Identify the **target** count: count of rows landed after the load completes
3. Compare source count to target count
4. Define a tolerance: exact match, or an acceptable variance (e.g. late-arriving
   data might mean a small negative variance is expected and not a failure)
5. If the variance exceeds tolerance, fail the check and alert — don't let the
   pipeline proceed silently

## What "good" looks like
- Source count == target count (or within agreed tolerance)
- The check runs automatically after every load, not manually/ad hoc
- A failure produces a clear, actionable alert (not just a log line nobody reads)

## Known limitations
- Row count matching alone does NOT prove the *right* rows arrived — two tables
  can have equal counts and still contain different data. Pair this with content-level
  checks (hashing, key-based diffing) for higher-stakes pipelines.
- Doesn't catch duplication that offsets missing rows (e.g. 2 rows dropped, 2 rows
  duplicated — count looks fine, but it's still wrong)