from fastapi import APIRouter
import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()
supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

@router.get("/")
def list_clients():
    result = supabase.table("clients") \
        .select("*") \
        .execute()
    return result.data