SELECT
    client_id,
    sku,
    location,
    quantity_on_hand,
    quantity_sold,
    reorder_point,
    last_counted_at,
    ingested_at,

    CASE
        WHEN quantity_on_hand <= 0 THEN 'STOCKOUT'
        WHEN quantity_on_hand < reorder_point THEN 'LOW_STOCK'
        WHEN quantity_sold = 0 THEN 'DEAD_STOCK'
        ELSE 'HEALTHY'
    END AS stock_status,

    CASE
        WHEN quantity_sold > 0
        THEN ROUND(CAST(quantity_on_hand AS FLOAT) / quantity_sold, 2)
        ELSE NULL
    END AS days_of_cover

FROM raw_inventory
WHERE client_id IS NOT NULL
  AND sku IS NOT NULL