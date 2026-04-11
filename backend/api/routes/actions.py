from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional, Dict
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

class ActionRequest(BaseModel):
    anomaly_id: str
    client_id: str
    action_type: str
    action_detail: Optional[Dict] = {}

@router.post("/execute")
def execute_action(req: ActionRequest):
    log_entry = {
        "anomaly_id": req.anomaly_id,
        "client_id": req.client_id,
        "action_type": req.action_type,
        "action_detail": req.action_detail,
        "executed_by": "operator"
    }
    result = supabase.table("actions_log") \
        .insert(log_entry) \
        .execute()
    return {
        "message": f"Action '{req.action_type}' logged.",
        "log_id": result.data[0]["id"]
    }

@router.get("/{anomaly_id}/history")
def get_action_history(anomaly_id: str):
    result = supabase.table("actions_log") \
        .select("*") \
        .eq("anomaly_id", anomaly_id) \
        .order("executed_at", desc=True) \
        .execute()
    return result.data