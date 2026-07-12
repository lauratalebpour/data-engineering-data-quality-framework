"""
Custom Expectation implementing patterns/completeness/row-count-reconciliation.md

Compares the row count of the table being validated against a reference table's
row count, failing if the difference exceeds an allowed tolerance percentage.

This is a simplified illustrative version — a production implementation would
extend GE's TableExpectation base class fully. Consultants adapting this into a
real client project should refer to GE's custom expectation documentation for
the complete class structure.
"""

from great_expectations.expectations.expectation import TableExpectation # type: ignore


class ExpectRowCountToReconcile(TableExpectation):
    """Fails if row count differs from a reference table beyond tolerance_pct."""

    examples = []

    metric_dependencies = ("table.row_count",)

    success_keys = ("reference_table_row_count", "tolerance_pct")

    default_kwarg_values = {
        "tolerance_pct": 0,
    }

    def _validate(self, metrics, configuration=None, **kwargs):
        actual_count = metrics["table.row_count"]
        reference_count = configuration.kwargs["reference_table_row_count"]
        tolerance_pct = configuration.kwargs.get("tolerance_pct", 0)

        allowed_diff = (tolerance_pct / 100.0) * reference_count
        row_diff = abs(actual_count - reference_count)

        return {
            "success": row_diff <= allowed_diff,
            "result": {
                "observed_value": actual_count,
                "reference_value": reference_count,
                "row_diff": row_diff,
            },
        }