import os
import time
import psycopg2


DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "password")


def initialize_database():
    while True:
        try:
            print("Trying to connect to PostgreSQL...", flush=True)

            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                connect_timeout=3,
            )

            cur = conn.cursor()

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS visit_counter (
                    id INTEGER PRIMARY KEY,
                    count INTEGER NOT NULL
                )
                """
            )

            cur.execute(
                """
                INSERT INTO visit_counter (id, count)
                VALUES (1, 0)
                ON CONFLICT (id) DO NOTHING
                """
            )

            conn.commit()

            cur.close()
            conn.close()

            print("Database initialization completed successfully.", flush=True)
            break

        except psycopg2.OperationalError as exc:
            print(f"PostgreSQL is not ready yet: {exc}", flush=True)
            print("Retrying in 3 seconds...", flush=True)
            time.sleep(3)


if __name__ == "__main__":
    initialize_database()
