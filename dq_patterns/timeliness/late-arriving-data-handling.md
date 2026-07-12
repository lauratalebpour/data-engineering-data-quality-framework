# Pattern: Late-Arriving Data Handling

**Dimension:** Timeliness

## The problem
Not all data arrives on schedule — a source system delay, a batch job retry, or a
downstream dependency running late can mean data intended for one time window
arrives after the pipeline has already processed and closed that window. Without
handling for this, late data either gets silently dropped or incorrectly bucketed
into the wrong period.

## When to use it
- Any pipeline with defined processing windows (daily batches, hourly loads) where
  the source system's availability isn't fully within your control
- Especially relevant for pipelines feeding regulatory or financial reporting,
  where a missed record has compliance implications, not just a reporting nuisance

## How it works
1. Define what counts as "late" — data arriving after its expected window has closed
2. Decide a grace period: how long after window close will late data still be
   accepted and reprocessed into the correct period
3. Implement a mechanism to detect late arrivals (compare event timestamp to
   processing timestamp) and route them appropriately — either an automatic
   reprocessing trigger or a flagged exception queue
4. Track the volume and pattern of late arrivals — persistent lateness from a
   specific source usually points to an upstream issue worth escalating

## What "good" looks like
- Late data within the agreed grace period is captured correctly, not silently lost
- Data arriving outside the grace period is explicitly flagged, not quietly merged
  into the wrong period
- Lateness trends are visible, not just individual incidents

## Known limitations
- Requires a reliable event timestamp from source — if the source only provides
  a processing timestamp, true lateness can't be measured
- A grace period that's too generous can delay reporting; too strict can create
  unnecessary reprocessing overhead — this trade-off should be agreed with the client