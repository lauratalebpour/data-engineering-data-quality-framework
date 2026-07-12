{% test row_count_reconciliation(model, compare_model, tolerance_pct=0) %}

-- Implements patterns/completeness/row-count-reconciliation.md
-- Fails (returns a row) if the row count difference between `model` and
-- `compare_model` exceeds the allowed tolerance percentage.

with source_count as (
    select count(*) as row_count from {{ compare_model }}
),

target_count as (
    select count(*) as row_count from {{ model }}
),

comparison as (
    select
        source_count.row_count as source_rows,
        target_count.row_count as target_rows,
        abs(source_count.row_count - target_count.row_count) as row_diff,
        {{ tolerance_pct }} / 100.0 * source_count.row_count as allowed_diff
    from source_count
    cross join target_count
)

select *
from comparison
where row_diff > allowed_diff

{% endtest %}