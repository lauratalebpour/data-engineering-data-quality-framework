-- Minimal example staging model.
-- In a real client project this would select/rename from a raw source table.
select
    customer_id,
    customer_name,
    email,
    country_code,
    created_at
from {{ source('raw', 'customers') }}