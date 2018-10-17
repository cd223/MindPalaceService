import os
import psycopg2
import urllib.parse as urlparse
from flask import Flask, jsonify

app = Flask(__name__)

def get_db_connection():
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port
    connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    return cursor.fetchall()

def get_data(query):
    connection = ""
    try:
        connection = get_db_connection()
    except:
        response = {"err": "Unable to connect to the database"}
        return jsonify(response), 404

    try:
        response = execute_query(connection, query)
    except:
        response = {"err": "General SQL Error"}
        return jsonify(response), 404
    return jsonify(response), 200

@app.route('/notes', methods=['GET'])
def get_notes():
    data = get_data("""SELECT * from note""")
    return data

@app.route('/users', methods=['GET'])
def get_users():
    data = get_data("""SELECT * from users""")
    return data

@app.route('/palaces', methods=['GET'])
def get_palaces():
    data = get_data("""SELECT * from palace""")
    return data

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)