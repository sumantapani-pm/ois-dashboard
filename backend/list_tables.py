import duckdb

conn = duckdb.connect('inventory.duckdb')
tables = conn.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='main'").fetchall()

for table in tables:
    print(table[0])

conn.close()
