from fastapi import APIRouter
from supabase import create_client
import os

router = APIRouter()

@router.get("/metrics")
def get_metrics(client_id: str):
    """Fetch operational metrics for a client"""
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_ANON_KEY")
    
    if not supabase_url or not supabase_key:
        return {"error": "Supabase credentials not configured"}
    
    supabase = create_client(supabase_url, supabase_key)
    response = supabase.table("operational_metrics").select("*").eq("client_id", client_id).execute()
    
    if not response.data:
        return {"error": "No metrics found"}
    
    row = response.data[0]
    return {
        "client_id": row["client_id"],
        "stockout_risk": row["stockout_risk_percent"],
        "overstock_burden": row["overstock_burden_percent"],
        "days_of_cover": row["avg_days_of_cover"],
        "timestamp": row["metrics_calculated_at"]
    }
