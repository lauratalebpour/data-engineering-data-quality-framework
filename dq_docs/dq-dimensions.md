# Data Quality Dimensions

Every data quality check maps to one of six dimensions. Use this table to classify
new checks and to explain issues to clients in consistent language.

| Dimension     | Question it answers                          | Example failure                          |
|---------------|-----------------------------------------------|-------------------------------------------|
| Completeness  | Is required data missing?                    | Null values in a mandatory column          |
| Accuracy      | Does the data reflect real-world truth?       | Outdated customer address                 |
| Consistency   | Does the same fact agree across systems?      | Different values for the same field in two systems |
| Validity      | Does data conform to expected format/rules?   | Non-numeric value in a numeric field       |
| Uniqueness    | Is there unwanted duplication?                | Same entity recorded more than once        |
| Timeliness    | Is the data current enough to be useful?      | Stale data presented as real-time          |

## Why this matters for this framework
Every check in `dbt/`, `great_expectations/`, and `soda/` should be traceable back to
one of these dimensions. When scoping DQ work with a client, start by asking which
dimensions matter most for their use case — not every project needs all six.
