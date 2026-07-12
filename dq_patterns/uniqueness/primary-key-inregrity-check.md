# Pattern: Primary Key Integrity Check

**Dimension:** Uniqueness

## The problem
A primary key is supposed to uniquely and reliably identify each row. When that
guarantee breaks — through a bad merge, a schema change, or a flawed load process —
every downstream join or aggregation built on that key becomes unreliable, often
without any obvious symptom until numbers stop adding up.

## When to use it
- On every table that has a defined primary key, as a standing, non-negotiable
  check — this is one of the few checks that should almost always run
- Especially critical directly after any schema change, migration, or change to
  the load process that generates or assigns the key

## How it works
1. Confirm the primary key field(s) for the table (single column or composite key)
2. Check that the key is never null (see also: Null / Mandatory Field Check)
3. Check that the key is unique — no two rows share the same key value(s)
4. Run this check as a hard gate: if it fails, the pipeline should stop rather than
   continue loading downstream, since everything after this point depends on the
   key being sound

## What "good" looks like
- 100% uniqueness and 100% non-null on the primary key, with zero tolerance —
  unlike some other checks, this one usually shouldn't have a "grace" threshold
- Failures block the pipeline rather than just being logged

## Known limitations
- A composite key can pass this check while still being a poor modeling choice
  (technically unique, but not meaningfully aligned to a real-world entity) —
  that's a data modeling concern, not something this check alone resolves
- Doesn't catch duplicate *entities* with different key values (see Duplicate
  Detection pattern for that case)