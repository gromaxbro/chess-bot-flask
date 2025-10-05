import psycopg2

# Replace with your Render Postgres External Database URL
DATABASE_URL = "postgresql://data_store_7lzv_user:0xZ0gSg6Lp6bcG15g9XkRFL1mjZLT161@dpg-d3ekj2r3fgac7389ua2g-a.oregon-postgres.render.com:5432/data_store_7lzv"

conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()

ngrok_url = "https://1234-abcd.ngrok-free.app"

a = 1;
cur.execute("SELECT DATE(updated_at),TIME(updated_at) FROM ngrok_url ;")
row = cur.fetchone()
print(row[0])  # prints the first row only
