# Data Engineering Data Quality Framework

A standardized approach to embedding data quality into data engineering
pipelines — built for consultants working across a variety of clients,
platforms, and tools.

## What this is (and isn't)
This repo is reference material, not a running project. Nothing here connects
to a live warehouse or a real pipeline. It exists to be read, copied, and
adapted into an actual client codebase — think of it as a cookbook, not a
kitchen.

## Start here
If you're new to this repo, read in this order:

1. **`docs/`** — what the six data quality dimensions mean, and why they're
   the shared vocabulary for everything else in this repo
2. **`patterns/`** — reusable, tool-agnostic designs for common DQ problems,
   organized by dimension. This is the core thinking behind every check in
   this repo
3. **Whichever of `dbt/`, `soda/`, or `great_expectations/`** matches your
   client's stack — each folder's README shows how the patterns above
   translate into that tool's syntax
4. **`examples/`** — full worked examples per platform (`aws_glue`,
   `databricks`, `snowflake`), showing all three tools running against the
   same checks in a realistic pipeline context
5. **`how-to/`** — task-specific guides for a given moment in an engagement:
   onboarding a client, running a rules workshop, setting up CI, handling a
   schema change, and more

## How the folders relate

| Folder | Answers | Tool/platform specific? |
|---|---|---|
| `docs/` | What does "data quality" mean here? | No |
| `patterns/` | What's the reusable design for this DQ problem? | No |
| `dbt/`, `soda/`, `great_expectations/` | How do I write this check in tool X? | Tool-specific, platform-agnostic |
| `examples/` | What does this look like end-to-end on platform Y? | Both |
| `how-to/` | What do I actually do, step by step, right now? | Neither — process guidance |

Every check in this repo, regardless of tool or platform, traces back to a
pattern doc. When in doubt about *why* a check exists, that's where to look.

## Folder structure