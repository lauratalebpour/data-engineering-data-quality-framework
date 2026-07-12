# Pattern: Expected Record Count by Category

**Dimension:** Completeness

## The problem
A table can pass a simple total row count check while still being incomplete —
if 500 rows are missing from Category A but 500 extra rows appear in Category B,
the total looks fine but the data is materially wrong. This is common when a
pipeline processes multiple categories, regions, or business units in one run and
one silently fails partway through.

## When to use it
- Any pipeline that processes data across distinct segments (regions, product
  lines, business units, currencies) in a single load
- Especially useful when historical volumes per category are predictable enough
  to set a baseline expectation

## How it works
1. Establish a baseline expected count (or range) per category, based on historical
   trends — e.g. average daily volume per region over the last 4 weeks
2. After each load, compare actual count per category against the baseline
3. Set a tolerance band (e.g. +/- 20%) rather than an exact match, since natural
   day-to-day variance is expected
4. Flag any category outside the tolerance band individually — don't rely on the
   total-row-count check to catch this

## What "good" looks like
- Every category's count falls within its expected band
- A breach in one category is investigated on its own, not masked by totals from
  other categories

## Known limitations
- Requires enough historical data to establish a meaningful baseline — not useful
  for a brand-new feed with no track record
- Genuine business changes (a client's new product launch, seasonal spikes) will
  trigger false alarms unless the baseline is updated to reflect known changes