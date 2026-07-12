# Pattern: Business Rule Validation

**Dimension:** Validity

## The problem
Some validity rules can't be expressed as a simple format pattern — they depend on
relationships between fields or specific business logic (an end date can't be
before a start date, a discount can't exceed 100%, a status can't skip a required
prior stage). Data can be well-formatted and still violate these rules.

## When to use it
- Any field or combination of fields governed by a business rule that a client has
  explicitly defined, rather than a generic format standard
- Especially important in workflow or state-based data, where valid transitions
  matter as much as valid individual values

## How it works
1. Work with the client to explicitly document the business rule — don't infer it;
   ambiguous or assumed rules are a common source of false failures
2. Translate the rule into a testable condition (e.g. `end_date >= start_date`)
3. Run the check against every relevant record
4. Fail or flag records that violate the rule, with enough context to identify why

## What "good" looks like
- Zero violations of hard business rules, or an explicitly agreed and documented
  list of known exceptions
- Rules are version-controlled and dated, so a rule change doesn't look like a
  spike in bad data

## Known limitations
- Business rules can and do change — a rule that was correct last quarter may be
  outdated now, so this pattern depends on ongoing communication with the client,
  not a one-time requirements exercise
- Complex multi-field rules can be difficult to express clearly in some DQ tools;
  may require custom logic rather than out-of-the-box checks