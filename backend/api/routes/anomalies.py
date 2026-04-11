from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

VALID_TRANSITIONS = {
    "open":        ["assigned"],
    "assigned":    ["in_progress", "open"],
    "in_progress": ["resolved"],
    "resolved":    ["verified", "open"],
    "verified":    []
}

class AnomalyUpdate(BaseModel):
    status: str
    assigned_to: Optional[str] = None
    resolution_note: Optional[str] = None
    metric_post_action: Optional[float] = None

@router.get("/")
def list_anomalies(client_id: str,
                   status: Optional[str] = None):
    query = supabase.table("anomalies") \
        .select("*") \
        .eq("client_id", client_id) \
        .order("created_at", desc=True)
    if status:
        query = query.eq("status", status)
    result = query.execute()
    return result.data

@router.get("/{anomaly_id}")
def get_anomaly(anomaly_id: str):
    result = supabase.table("anomalies") \
        .select("*") \
        .eq("id", anomaly_id) \
        .single() \
        .execute()
    if not result.data:
        raise HTTPException(status_code=404,
                           detail="Anomaly not found")
    return result.data

@router.patch("/{anomaly_id}/status")
def update_anomaly_status(anomaly_id: str,
                          update: AnomalyUpdate):
    current = supabase.table("anomalies") \
        .select("status, client_id") \
        .eq("id", anomaly_id) \
        .single() \
        .execute()

    if not current.data:
        raise HTTPException(status_code=404,
                           detail="Anomaly not found")

    current_status = current.data["status"]
    new_status = update.status

    if new_status not in VALID_TRANSITIONS.get(
            current_status, []):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid transition: "
                   f"{current_status} → {new_status}. "
                   f"Allowed: "
                   f"{VALID_TRANSITIONS[current_status]}"
        )

    payload = {"status": new_status}
    if update.assigned_to:
        payload["assigned_to"] = update.assigned_to
    if update.resolution_note:
        payload["resolution_note"] = update.resolution_note
    if update.metric_post_action is not None:
        payload["metric_post_action"] = \
            update.metric_post_action
    if new_status == "verified":
        from datetime import datetime, timezone
        payload["verified_at"] = \
            datetime.now(timezone.utc).isoformat()

    supabase.table("anomalies") \
        .update(payload) \
        .eq("id", anomaly_id) \
        .execute()

    return {
        "message": f"Status updated: "
                   f"{current_status} → {new_status}"
    }