# How-to: Onboarding a New Client

Use this the first time you're setting up data quality work on a new
engagement — from first conversation to first working check.

## 1. Scope which dimensions matter
Not every client needs all six DQ dimensions (`docs/dq-dimensions.md`) covered
equally. Ask the client (or infer from the engagement brief):
- What's the primary pain point — missing data, wrong data, duplicate data,
  stale data, or inconsistency across systems?
- Is this feeding regulatory or financial reporting (raises the bar on
  completeness and accuracy), or an internal analytics use case (more
  tolerance for soft gates)?

Don't try to cover everything on day one. Pick the 1-2 dimensions the client
actually cares about and start there.

## 2. Identify the platform
Check which of `examples/aws_glue`, `examples/databricks`, or
`examples/snowflake` matches the client's stack. If none match exactly, the
closest platform's example is still your best starting reference — the checks
and patterns are platform-agnostic even when the plumbing isn't.

## 3. Choose a tool
If the client already has dbt, Great Expectations, or Soda in place, use it —
don't introduce a second tool without a clear reason. If nothing is in place
yet, see `how-to/choosing-a-tool.md` for the full decision guide.

## 4. Identify a first table to check
Pick something small, well-understood, and low-risk for the first
implementation — not the most critical pipeline in the business. The goal of
the first check is to prove the pattern works end-to-end (extract → check →
gate → alert), not to cover every table on day one.

## 5. Map the first checks to patterns
For the first table, walk through `patterns/` and identify which apply.
Primary Key Integrity and Null/Mandatory Field checks are almost always a safe
starting pair — they're simple, they're hard gates, and they immediately
demonstrate value.

## 6. Implement, using the matching tool README
Follow the setup steps in the relevant `dbt/README.md`, `soda/README.md`, or
`great_expectations/README.md`, adapting the `customers`-based examples to the
client's actual table and columns.

## 7. Decide gating behaviour with the client, not for them
Before going live, explicitly agree with the client which checks are hard
gates (block the pipeline) vs. soft gates (alert and continue). Don't assume —
get this in writing, even informally in a workshop or email. This decision
has real operational consequences if you get it wrong.

## 8. Document what you built
Add an entry to the client's own documentation (not this repo) linking each
check back to the pattern it implements. If you build something genuinely new
along the way — a pattern not yet in `patterns/`, or a platform-specific
technique — consider contributing it back into this framework so the next
consultant benefits.