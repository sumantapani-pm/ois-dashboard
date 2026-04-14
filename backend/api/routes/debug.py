from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/debug-env")
def debug_env():
    return {
        "SUPABASE_URL": os.getenv("SUPABASE_URL", "NOT SET"),
        "SUPABASE_ANON_KEY": os.getenv("SUPABASE_ANON_KEY", "NOT SET")[:50] if os.getenv("SUPABASE_ANON_KEY") else "NOT SET"
    }
