# How-to: Choosing a Tool

Use this when a client has no DQ tool in place yet and you need to make a
real recommendation — not just "any of them would work."

## Start here: does the client already have something?
If dbt, Great Expectations, or Soda is already in use anywhere in the client's
stack — even informally, even by one team — default to that. Introducing a
second DQ tool alongside an existing one is rarely worth the maintenance
overhead, and almost never worth it just because you personally prefer a
different tool.

If nothing is in place, use the trade-offs below.

## dbt
**Choose when:**
- The client's pipeline is already SQL-transformation-heavy and dbt-centric,
  or is about to become so
- The team is comfortable with SQL but less so with Python
- Checks need to live right next to the models they validate, in the same
  codebase and PR review process

**Real trade-offs:**
- Checks are tightly coupled to models — great for cohesion, but it means DQ
  can't easily run independently of a dbt run
- Custom logic (like row count reconciliation) requires writing a Jinja/SQL
  macro — approachable for a SQL-strong team, awkward for anything genuinely
  complex
- No native reporting/dashboard output — failures show up in `dbt test`
  output and CI logs only, unless you build something extra

## Great Expectations
**Choose when:**
- The team is Python-strong and anticipates complex, custom validation logic
  beyond what a line of YAML or SQL can express cleanly
- Client stakeholders want a readable, browsable report of check results
  (Data Docs), not just pass/fail in a log
- Checks need to run independently of any specific transformation tool — GE
  doesn't assume dbt, Spark, or any particular pipeline shape

**Real trade-offs:**
- Steepest learning curve of the three — suites, checkpoints, data contexts,
  and batch requests are new concepts even for confident Python users
- More setup overhead for simple cases — a single not-null check is more
  ceremony in GE than in dbt or Soda
- Most powerful option when logic gets genuinely complex, but that power isn't
  free

## Soda
**Choose when:**
- Non-engineers (analysts, business stakeholders) need to read or even write
  checks themselves — SodaCL reads closest to plain English of the three
- You need something running fast, with minimal setup, especially for an
  early-stage or proof-of-concept engagement
- The client's stack spans multiple platforms and you want one consistent
  checks syntax across all of them (see `examples/` — Soda is the one tool
  we've shown running identically across Glue, Databricks, and Snowflake)

**Real trade-offs:**
- Weakest of the three for genuinely custom, complex logic — user-defined SQL
  checks work but lack the reusable structure dbt's macros or GE's custom
  expectations offer
- Less mature ecosystem/community than dbt specifically
- Free tier is check-execution only; a fuller reporting/monitoring experience
  usually means Soda Cloud, a paid product — confirm this is acceptable to
  the client before committing

## If you're still unsure
Default to whichever tool the client's engineers will actually maintain after
you leave. A technically ideal tool that a client team resents or abandons
within three months is worse than a "good enough" tool they keep using. Ask
directly: "which of these would your team actually want to own long-term?"