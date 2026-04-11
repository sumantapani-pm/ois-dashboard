import duckdb
import os

DB_PATH = os.getenv("DUCKDB_PATH", "data/ois.duckdb")

def get_connection():
    return duckdb.connect(DB_PATH)

def initialize_db():
    con = get_connection()
    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_inventory (
            client_id       VARCHAR,
            sku             VARCHAR,
            location        VARCHAR,
            quantity_on_hand INTEGER,
            quantity_sold   INTEGER,
            reorder_point   INTEGER,
            last_counted_at TIMESTAMP,
            ingested_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.execute("""
        CREATE TABLE IF NOT EXISTS raw_fulfillment (
            client_id       VARCHAR,
            order_id        VARCHAR,
            promised_date   DATE,
            actual_date     DATE,
            status          VARCHAR,
            ingested_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    con.close()
    print("Database initialized.")

if __name__ == "__main__":
    initialize_db()