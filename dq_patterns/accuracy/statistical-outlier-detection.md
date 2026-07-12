# Pattern: Statistical Outlier Detection

**Dimension:** Accuracy

## The problem
Some inaccurate values aren't invalid or incomplete — they're plausible-looking
numbers that are simply wrong (a transaction amount entered with an extra zero,
an age of 150, a negative price). These pass format and completeness checks but
still don't reflect reality.

## When to use it
- Numeric fields where an expected range or distribution can be reasonably defined
  (amounts, quantities, durations, ages)
- Useful as a second-line check after format/completeness checks have already
  passed — this catches what those checks structurally cannot

## How it works
1. Establish the expected distribution for the field, using historical data
   (mean, standard deviation, or a simple min/max business rule)
2. Define an outlier threshold — commonly a number of standard deviations from
   the mean, or a hard business-defined bound (e.g. "no transaction should exceed X")
3. Flag values outside the threshold for review — outlier detection should flag,
   not auto-correct, since some outliers are genuine
4. Review flagged outliers periodically to refine the threshold over time

## What "good" looks like
- Genuine outliers are caught and routed for human review before they reach
  reporting
- The false-positive rate is low enough that reviewers trust the flags rather
  than ignoring them

## Known limitations
- A statistically "normal" value can still be factually wrong, and a genuine
  outlier (a real, unusually large transaction) can be flagged incorrectly —
  this check narrows the search, it doesn't replace judgment
- Thresholds need periodic recalibration as the underlying business changes