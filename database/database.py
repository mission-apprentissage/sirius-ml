import psycopg2

class DB():
    def __init__(self, db=''):
        # Initialize database
        self.db = db
        self.table = None
        print("[Done] Database initialized.")

    def load(self, table=''):
        conn = psycopg2.connect(self.db)
        cur = conn.cursor()
        print("[Done] Connected to database.")

        # Load table
        self.table = table
        print(f"[Pending] Loading {table} table...")
        query = f"SELECT * FROM {table}"
        cur.execute(query)
        datapoints = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        cur.close()
        print(f"[Done] {table} table loaded.")
        return {'datapoints': datapoints, 'cols': cols}