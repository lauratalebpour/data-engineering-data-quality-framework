# Pattern: Freshness SLA Check

**Dimension:** Timeliness

## The problem
Data can be complete, accurate, and well-formatted, and still be too old to be
useful — a dashboard showing "current" inventory that's actually 3 days stale, or
a report built on a feed that silently stopped updating. Without an explicit
freshness check, staleness is invisible until someone notices the numbers look
suspiciously unchanged.

## When to use it
- Any dataset with a defined expectation for how current it should be (real-time,
  hourly, daily) — this expectation should come from how the data is actually used
  downstream, not an arbitrary technical default
- Particularly important for feeds with external dependencies (vendor files,
  third-party APIs) where an upstream outage is outside your direct control

## How it works
1. Agree the freshness SLA with the client — how old is "too old" for this data's
   use case
2. Identify a reliable timestamp to measure against (last updated time, max event
   timestamp in the table, or last successful load time)
3. On a schedule, compare current time against that timestamp
4. If the gap exceeds the SLA, trigger an alert — this should be proactive
   (checked on a schedule) rather than only discovered when someone queries the data

## What "good" looks like
- The dataset is always within its agreed freshness SLA, or breaches are alerted
  on immediately rather than discovered downstream
- The check runs independently of the load process, so a load that silently stops
  running entirely is still caught

## Known limitations
- Doesn't tell you *why* data is stale — that requires separate pipeline
  monitoring/observability, this check only tells you *that* it's stale
- SLA definitions can vary significantly by use case within the same client, so
  don't assume one freshness standard applies across every table