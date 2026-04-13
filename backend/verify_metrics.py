import duckdb

conn = duckdb.connect('../data/ois.duckdb')

# Check if view exists and has data
result = conn.execute("SELECT * FROM operational_metrics LIMIT 5").fetchall()

print("Operational Metrics Data:")
print()

if len(result) == 0:
    print("No data")
else:
    for row in result:
        print(f"Client: {row[0]}")
        print(f"  Stockout Risk: {row[1]}%")
        print(f"  Overstock Burden: {row[2]}%")
        print(f"  Avg Days of Cover: {row[3]}")
        print()

conn.close()
