# Pattern: Derived Field Recalculation Check

**Dimension:** Consistency

## The problem
Many fields are calculated from other fields — a total from line items, a status
from a set of business rules, an age from a date of birth. Over time, the stored
derived value and the fields it was calculated from can drift out of sync (a line
item is updated but the total isn't recalculated), leaving an internally
inconsistent record.

## When to use it
- Any table storing a derived/calculated field alongside its source fields, rather
  than calculating it on the fly at query time
- Particularly important after any update or backfill process that touches the
  source fields but might not trigger recalculation

## How it works
1. Identify the derivation logic — the exact rule used to calculate the stored field
2. Independently recalculate the expected value from the source fields, using the
   same logic
3. Compare the recalculated value to the stored value
4. Flag mismatches, and decide handling: automatically recalculate and overwrite,
   or flag for review if the discrepancy might indicate a deeper logic error

## What "good" looks like
- Stored and recalculated values match for (effectively) all records
- Mismatches are traced to a specific cause — a missed recalculation trigger vs.
  a genuine bug in the derivation logic — not just silently patched

## Known limitations
- Requires the derivation logic to be documented and stable — if the business rule
  itself is ambiguous or has changed without being recorded, this check will
  produce noisy, unreliable results
- Recalculating at scale can be computationally expensive; consider sampling for
  very large tables rather than checking every record on every run