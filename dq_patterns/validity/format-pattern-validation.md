# Pattern: Format / Pattern Validation

**Dimension:** Validity

## The problem
Fields often have an implicit or explicit expected format — an email address
containing "@", a postcode matching a national format, a date in a consistent
format. Even when a field is populated (passes a completeness check), it can still
be unusable if it doesn't conform to the format downstream systems expect.

## When to use it
- Any field with a well-defined format standard (email, phone number, postcode,
  currency code, date format)
- Particularly important at ingestion, before format errors propagate into
  transformations that assume well-formed input

## How it works
1. Define the expected format as a pattern (regex, data type, or an allowed value
   list, depending on the field)
2. Validate every non-null value against the pattern
3. Decide handling for non-conforming values: reject, flag for review, or attempt
   automated correction (only for well-understood, low-risk cases — e.g. trimming
   whitespace)
4. Track the non-conformance rate over time, not just per run — a rising trend
   often signals an upstream system change

## What "good" looks like
- Non-conformance rate at or below an agreed threshold
- Failures are specific about *which* rule was violated, not just "invalid"

## Known limitations
- A value can match the expected format and still be wrong (a syntactically valid
  but non-existent email address) — this is a validity check, not an accuracy check
- Overly strict patterns can generate false positives on legitimate edge cases
  (e.g. valid but unusual international phone formats) — test against real data
  before deploying