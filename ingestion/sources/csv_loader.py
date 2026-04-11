import duckdb
import pandas as pd
import sys
import os
from datetime import datetime, timezone

def load_inventory_csv(client_id: str, file_path: str):
    df = pd.read_csv(file_path)
    df['last_counted_at'] = pd.to_datetime(df['last_counted_at'])
    df['client_id'] = client_id
    df['ingested_at'] = datetime.now(timezone.utc)

    # Reorder columns to exactly match the table schema
    df = df[[
        'client_id',
        'sku',
        'location',
        'quantity_on_hand',
        'quantity_sold',
        'reorder_point',
        'last_counted_at',
        'ingested_at'
    ]]

    con = duckdb.connect("data/ois.duckdb")
    con.execute("DELETE FROM raw_inventory WHERE client_id = ?", [client_id])
    con.execute("INSERT INTO raw_inventory SELECT * FROM df")
    count = con.execute(
        "SELECT COUNT(*) FROM raw_inventory WHERE client_id = ?",
        [client_id]
    ).fetchone()[0]
    con.close()
    print(f"Loaded {count} inventory rows for client: {client_id}")

if __name__ == "__main__":
    client_id = sys.argv[1]
    file_path = sys.argv[2]
    load_inventory_csv(client_id, file_path)