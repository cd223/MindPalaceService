import os
import psycopg2
import json
import urllib.parse as urlparse
from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor

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

def get_data(query):
    connection = ""
    try:
        connection = get_db_connection()
    except:
        response = {"Error": "Unable to connect to the database"}
        return jsonify(response), 404
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query)
        response = cursor.fetchall()
    except:
        response = {"Error": "General SQL error"}
        cursor.close()
        connection.close()
        return jsonify(response), 404
    cursor.close()
    connection.close()
    return jsonify(response), 200

def insert_data(query, data):
    connection = ""
    try:
        connection = get_db_connection()
    except:
        response = {"Error": "Unable to connect to the database"}
        return jsonify(response), 404
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, data)
        connection.commit()
    except:
        response = {"Error": "General SQL error"}
        cursor.close()
        connection.close()
        return jsonify(response), 404
    cursor.close()
    connection.close()
    return jsonify(response), 200


@app.route('/notes', methods=['GET'])
def notes():
    data = get_data("""SELECT * from note;""")
    return data

@app.route('/note/<note_id>', methods=['GET', 'DELETE'])
def note(note_id):
    if request.method == 'GET':
        data = get_data("""SELECT * from note WHERE note_id={};""".format(note_id))
        return data
    if request.method == 'DELETE':
        data = get_data("""DELETE * from note WHERE user_id={};""".format(note_id))
        return data

# TODO: Add logic for adding new note
@app.route('/newnote', methods=['POST'])
def new_note():
    req_data = request.get_json()
    return req_data, 200


@app.route('/users', methods=['GET'])
def users():
    data = get_data("""SELECT * from users;""")
    return data

@app.route('/user/<user_id>', methods=['GET', 'DELETE'])
def user(user_id):
    if request.method == 'GET':
        data = get_data("SELECT * from users WHERE user_id={};".format(user_id))
        return data
    if request.method == 'DELETE':
        data = get_data("""DELETE * from users WHERE user_id={};""".format(user_id))
        return data

@app.route('/newuser', methods=['POST'])
def new_user():
    req_data = request.get_json()
    user_name = req_data['user_name']
    user_username = req_data['user_username']
    user_password = req_data['user_password']
    insert_data("""INSERT INTO users (user_name, user_username, user_password) VALUES (%s, %s, %s);""", (user_name, user_username, user_password))
    return "Success", 200


@app.route('/palaces', methods=['GET'])
def palaces():
    data = get_data("""SELECT * from palace""")
    return data

@app.route('/palace/<palace_id>', methods=['GET', 'DELETE'])
def palace(palace_id):
    if request.method == 'GET':
        data = get_data("SELECT * from palace WHERE palace_id={};".format(palace_id))
        return data
    if request.method == 'DELETE':
        data = get_data("DELETE * from palace WHERE user_id={};".format(palace_id))
        return data

# TODO: Add logic for adding new palace
@app.route('/newpalace', methods=['POST'])
def new_palace():
    req_data = request.get_json()
    return req_data, 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)