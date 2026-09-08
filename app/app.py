import os
from flask import Flask, jsonify
import psycopg2
from psycopg2 import OperationalError

app = Flask(__name__)

DB_HOST = os.getenv('DB_HOST', 'postgres-service')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'appdb')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')


def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        connect_timeout=3,
    )


def initialize_database():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS visit_counter (
                id INTEGER PRIMARY KEY,
                count INTEGER NOT NULL
            )
        ''')
        cur.execute('''
            INSERT INTO visit_counter (id, count)
            VALUES (1, 0)
            ON CONFLICT (id) DO NOTHING
        ''')
        conn.commit()
        cur.close()
        conn.close()
    except OperationalError as exc:
        print(f'Database is not ready yet: {exc}', flush=True)


@app.route('/')
def home():
    return jsonify(
        application='devops-kubernetes-demo',
        message='Application is running successfully',
        endpoints=['/visits', '/health/live', '/health/ready']
    )


@app.route('/health/live')
def liveness():
    # This checks only whether the Flask process can answer requests.
    return jsonify(status='alive'), 200


@app.route('/health/ready')
def readiness():
    # Ready means the application can also reach its required database.
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.fetchone()
        cur.close()
        conn.close()
        return jsonify(status='ready', database='reachable'), 200
    except OperationalError as exc:
        return jsonify(status='not-ready', database='unreachable', error=str(exc)), 503


@app.route('/visits')
def visits():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO visit_counter (id, count)
            VALUES (1, 1)
            ON CONFLICT (id)
            DO UPDATE SET count = visit_counter.count + 1
            RETURNING count
        ''')
        count = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return jsonify(visits=count), 200
    except OperationalError as exc:
        return jsonify(error='Database connection failed', details=str(exc)), 500


if __name__ == '__main__':
    initialize_database()
    app.run(host='0.0.0.0', port=5000)
