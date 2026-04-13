import duckdb

conn = duckdb.connect('../data/ois.duckdb')
result = conn.execute("DESCRIBE stg_inventory").fetchall()

print("Columns in stg_inventory:")
for row in result:
    print(f"  {row[0]} ({row[1]})")

conn.close()
