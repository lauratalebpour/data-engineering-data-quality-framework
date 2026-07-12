# Pattern: Null / Mandatory Field Check

**Dimension:** Completeness

## The problem
Certain fields must always have a value for a record to be usable — a customer ID,
a transaction date, an account number. When these fields go unexpectedly null,
downstream joins silently drop records, reports undercount, or processes fail in
ways that are hard to trace back to the root cause.

## When to use it
- On any field a client has defined as "mandatory" for business or regulatory reasons
- On join keys and foreign keys, even if not explicitly flagged as mandatory —
  a null key breaks referential logic
- Early in a pipeline (staging layer), so bad data is caught before it propagates

## How it works
1. Define the list of fields considered mandatory for a given table (this should come
   from the client, not be assumed)
2. For each mandatory field, check the proportion (or count) of null values
3. Set a threshold — for true mandatory fields this is usually 0% tolerance, but some
   fields may have an agreed acceptable null rate (e.g. an optional-but-preferred field)
4. Fail the check if nulls exceed the threshold; log which records are affected so
   they can be traced back to source

## What "good" looks like
- 0% nulls on hard-mandatory fields (or within agreed tolerance)
- Failing records are identifiable, not just counted — you need to know *which* rows,
  not just *how many*

## Known limitations
- A field can be "not null" and still be wrong (e.g. a placeholder value like "N/A"
  or "0000-00-00" instead of a true null) — pair with a Validity check to catch these
- Doesn't tell you *why* the value is missing — that's a data lineage/root cause task