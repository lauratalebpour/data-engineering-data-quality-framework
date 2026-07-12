# How-to: Handling a Schema Change

Use this when a client's source system changes shape — a new column appears,
an existing one is renamed or retyped, or a table is restructured — and your
DQ checks need to keep up.

## Why this matters more than it seems
Schema changes don't always cause loud failures. Two silent failure modes are
more dangerous than a check that errors out clearly:
- **A renamed column stops a check from running at all** — no error, just
  silent non-coverage. `not_null` on a column that no longer exists doesn't
  fail loudly in every tool; sometimes it just... stops checking anything
  meaningful
- **A retyped column passes checks that no longer mean what they used to** —
  e.g. a column that changed from a string to a numeric ID might still pass a
  format check, while breaking every downstream assumption

## Detecting a schema change happened
- If the client has schema versioning or change notifications (common in
  well-governed environments), that's your earliest signal — build a habit of
  checking it, don't assume you'll be told
- Absent that, a sudden spike or drop in a check's failure rate is often the
  first practical sign something upstream changed — this is why tracking
  trends over time (mentioned in several `patterns/` docs) matters, not just
  pass/fail on the latest run
- Row count patterns (`patterns/completeness/row-count-reconciliation.md`,
  `expected-record-count-by-category.md`) are often the fastest to catch a
  structural change, even before a column-level check does

## Responding to a confirmed schema change
1. **Confirm the change with the client/source team before touching
   anything** — don't guess at what changed; get the actual diff or
   changelog if possible
2. **Update the check definitions**, not just the underlying model/query —
   it's easy to fix a model's SQL and forget the YAML/checks file still
   references the old column name
3. **Re-run the full suite, not just the affected check** — a schema change
   in one column can ripple into checks on related columns (e.g. a renamed
   join key affects any relationship/reconciliation check using it)
4. **Update the pattern-mapping comments/meta fields** if the change affects
   what a check actually validates — stale comments claiming a check does
   something it no longer does are worse than no comment at all
5. **Log the change** somewhere the next consultant on this engagement will
   see it — a dated note in the client's own docs, not just a silent code fix

## Preventing repeat pain
Where the platform supports it, add a lightweight schema check ahead of your
DQ suite — confirming expected columns and types exist before running the
full check suite. This turns "checks silently stop meaning anything" into "a
clear, early failure: the schema changed." Not yet built into this repo's
examples — worth treating as a candidate for a new pattern
(`patterns/validity/` is the natural home) if you build one on a client
project.