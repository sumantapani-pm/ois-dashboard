import duckdb
import os
from supabase import create_client
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
DB_PATH = os.getenv("DUCKDB_PATH", "data/ois.duckdb")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def run_detection(client_id: str, client_slug: str):
    print(f"Running anomaly detection for {client_slug}...")

    rules = supabase.table("threshold_rules") \
        .select("*") \
        .eq("client_id", client_id) \
        .eq("is_active", True) \
        .execute()

    con = duckdb.connect(DB_PATH, read_only=True)
    new_anomalies = []

    for rule in rules.data:
        domain = rule["domain"]
        metric = rule["metric"]
        operator = rule["operator"]
        threshold = rule["threshold_value"]
        severity = rule["severity"]

        if domain == "inventory":
            op_symbol = (
                '<' if operator == 'less_than'
                else '>' if operator == 'greater_than'
                else '='
            )
            query = f"""
                SELECT sku as entity_id,
                       sku as entity_label,
                       {metric} as actual_value
                FROM stg_inventory
                WHERE client_id = '{client_slug}'
                  AND {metric} IS NOT NULL
                  AND {metric} {op_symbol} {threshold}
            """
            try:
                results = con.execute(query).fetchdf()
                for _, row in results.iterrows():
                    existing = supabase.table("anomalies") \
                        .select("id") \
                        .eq("client_id", client_id) \
                        .eq("metric", metric) \
                        .eq("entity_id", str(row["entity_id"])) \
                        .in_("status", ["open","assigned","in_progress"]) \
                        .execute()

                    if not existing.data:
                        new_anomalies.append({
                            "client_id": client_id,
                            "rule_id": rule["id"],
                            "domain": domain,
                            "metric": metric,
                            "entity_id": str(row["entity_id"]),
                            "entity_label": str(row["entity_label"]),
                            "threshold_value": float(threshold),
                            "actual_value": float(row["actual_value"]),
                            "severity": severity,
                            "status": "open"
                        })
            except Exception as e:
                print(f"Rule evaluation error: {e}")

    con.close()

    if new_anomalies:
        supabase.table("anomalies").insert(new_anomalies).execute()
        print(f"Inserted {len(new_anomalies)} new anomalies.")
    else:
        print("No new anomalies detected.")

if __name__ == "__main__":
    client = supabase.table("clients") \
        .select("id") \
        .eq("slug", "client-alpha") \
        .execute()

    if client.data:
        run_detection(
            client_id=client.data[0]["id"],
            client_slug="client_001"
        )