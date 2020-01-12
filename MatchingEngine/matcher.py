from MatchingEngine.db_connector import connectDB

conn = connectDB()
cur = conn.cursor()
cur.execute("select column_name,data_type from information_schema.columns where table_name = 'dex_order';")
row = cur.fetchall()
print(row)
cur.execute("select * from dex_sellorder JOIN dex_order ON dex_sellorder.order_ptr_id = dex_order.id;")
row = cur.fetchall()
print(row)
cur.execute("select * from dex_buyorder JOIN dex_order ON dex_buyorder.order_ptr_id = dex_order.id;")
row = cur.fetchall()
print(row)