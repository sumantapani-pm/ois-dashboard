
  
  create view "ois"."main"."operational_metrics__dbt_tmp" as (
    ﻿SELECT
    client_id,
    
    ROUND(
        (COUNT(CASE WHEN quantity_on_hand = 0 THEN 1 END)::FLOAT / 
         NULLIF(COUNT(*), 0)) * 100, 
        2
    ) AS stockout_risk_percent,
    
    ROUND(
        (SUM(CASE WHEN quantity_on_hand > reorder_point * 2 THEN quantity_on_hand ELSE 0 END)::FLOAT /
         NULLIF(SUM(quantity_on_hand), 0)) * 100,
        2
    ) AS overstock_burden_percent,
    
    ROUND(
        AVG(days_of_cover),
        2
    ) AS avg_days_of_cover,
    
    NOW() AS metrics_calculated_at

FROM stg_inventory
GROUP BY client_id
  );
