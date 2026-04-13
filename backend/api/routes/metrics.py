from fastapi import APIRouter
import duckdb

router = APIRouter()

@router.get("/metrics")
def get_metrics(client_id: str):
    """Fetch operational metrics for a client"""
    conn = duckdb.connect('../data/ois.duckdb')
    
    query = """
    SELECT 
        client_id,
        stockout_risk_percent,
        overstock_burden_percent,
        avg_days_of_cover,
        metrics_calculated_at
    FROM operational_metrics
    WHERE client_id = ?
    """
    
    result = conn.execute(query, [client_id]).fetchall()
    conn.close()
    
    if not result:
        return {"error": "No metrics found"}
    
    row = result[0]
    return {
        "client_id": row[0],
        "stockout_risk": row[1],
        "overstock_burden": row[2],
        "days_of_cover": row[3],
        "timestamp": str(row[4])
    }
