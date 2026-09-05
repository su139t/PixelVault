from flask import Flask, jsonify
from flask_cors import CORS

from db import get_db_connection


app = Flask(__name__)

CORS(app)


@app.get("/")
def home():
    return jsonify({
        "message": "PixelVault Backend Running"
    })


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "project": "PixelVault"
    })


@app.get("/api/db-test")
def db_test():
    try:
        conn = get_db_connection()

        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                    current_database(),
                    current_user,
                    version();
            """)

            result = cursor.fetchone()

        conn.close()

        return jsonify({
            "status": "success",
            "database": result[0],
            "user": result[1],
            "postgresql_version": result[2]
        })

    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )