# Pattern: Cross-System Consistency Check

**Dimension:** Consistency

## The problem
The same real-world fact often lives in more than one system — a customer's status
in a CRM vs a billing system, a balance in an operational database vs a downstream
warehouse. When these fall out of sync, different teams end up working from
different "truths," and nobody notices until a client asks why two reports disagree.

## When to use it
- Whenever the same entity or fact is sourced from, or duplicated across, more than
  one system feeding the same pipeline or reporting layer
- Particularly important during migrations, where old and new systems run in
  parallel and must be provably consistent before cutover

## How it works
1. Identify the shared entity/fact and the two (or more) systems that hold it
2. Define the matching key that links a record in System A to its counterpart in
   System B
3. Compare the value(s) in question field-by-field for matched records
4. Define what counts as a mismatch (exact match required, or acceptable variance —
   e.g. timing lag between systems)
5. Report mismatches with enough detail to investigate (both values, the key, and
   which system is presumed authoritative)

## What "good" looks like
- Mismatch rate at or below an agreed threshold
- Every mismatch is traceable to a specific record pair, not just a count
- A designated "source of truth" is documented for when systems disagree

## Known limitations
- Requires a reliable matching key across systems — if the key itself is inconsistent,
  this check can't run
- Timing differences (System A updates before System B) can look like real mismatches;
  build in a reasonable lag tolerance before flagging as a true failure