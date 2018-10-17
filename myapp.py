import os
import psycopg2
import urllib.parse as urlparse
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/notes')
def get_notes():
    conn = ""
    out = []
    try:
        url = urlparse.urlparse(os.environ['DATABASE_URL'])
        dbname = url.path[1:]
        user = url.username
        password = url.password
        host = url.hostname
        port = url.port
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    except:
        out = {"err": "Unable to connect to the database"}
        return jsonify(out), 404
        
    try:
        cur = conn.cursor()
        cur.execute("""SELECT * from note""")
        rows = cur.fetchall()
        out = []
        for row in rows:
            out.append({"id": row[0], "name": row[1]})
    except:
        out = {"err": "General SQL Error"}
        return jsonify(out), 404

    return jsonify(out), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)