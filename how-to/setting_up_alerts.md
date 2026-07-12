# How-to: Setting Up Alerting

Use this once checks are implemented and you need failures to actually reach
a human, rather than sitting silently in a scan log or CI output.

## 1. Confirm gating behaviour is already decided
Alerting design depends entirely on whether a check is a hard gate or a soft
gate (see `how-to/onboarding-a-new-client.md`, step 7). Don't design alerting
before this is settled — you'll likely have to redo it.

- **Hard gate failures** need alerting that reaches someone who can act
  immediately — the pipeline is stopped, and every minute it's stopped has a
  cost
- **Soft gate failures** can usually tolerate a slower channel — a daily
  digest, a dashboard, a ticket — since the pipeline is still running

## 2. Pick a channel that matches the client's existing tooling
Don't introduce a new alerting tool if the client already has one. Common
patterns:
- Slack/Teams webhook for immediate, human-readable alerts
- Email digest for lower-urgency, batched summaries
- A ticketing system (Jira, ServiceNow) if failures need to be tracked and
  assigned, not just seen

## 3. Make failure messages actionable, not just informative
A good failure alert answers three questions at a glance:
- **What failed** (which check, which table, which pattern it implements)
- **How badly** (how many records, what percentage, is this a first
  occurrence or a recurring issue)
- **What to do next** (who owns this table, where to look first)

A message that just says "DQ check failed" sends people straight to the logs
and erodes trust in the alerting system over time — they'll start ignoring it.

## 4. Set thresholds in a shared, central location
Avoid hardcoding thresholds directly in tool-specific check files where
possible — keeping them in a shared config makes it much easier to tune
sensitivity later without touching test/check code across three different
tools.

## 5. Avoid alert fatigue from day one
- Start with alerting only on hard gates; add soft-gate alerting once the
  team has shown they're acting on the hard-gate ones
- Review alert volume after the first 1-2 weeks live — if a check is firing
  constantly and nobody's acting on it, the threshold (or the rule itself) is
  probably wrong, not the team's attention span

## 6. Document the on-call/ownership path
Every alert should have an implicit or explicit answer to "whose problem is
this." If that's not already clear from the client's existing structure,
raise it as a gap during onboarding rather than assuming it'll sort itself
out once alerts start firing.