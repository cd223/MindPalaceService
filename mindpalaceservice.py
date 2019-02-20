import os
import psycopg2
import json
import urllib.parse as urlparse
from flask import Flask, jsonify, request
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import AsIs
import numpy as np
from numpy import random
from scipy.spatial.distance import cdist

app = Flask(__name__)

def closest_point(point, points):
    return points[cdist([point], points).argmin()]

def get_db_connection():
    url = urlparse.urlparse(os.environ['DATABASE_URL'])
    dbname = url.path[1:]
    user = url.username
    password = url.password
    host = url.hostname
    port = url.port
    connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
    return connection

def get_data(query, data, toJson):
    connection = ""
    try:
        connection = get_db_connection()
    except:
        response = {"Error": "Unable to connect to the database"}
        return jsonify(response), 505
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, data)
        response = cursor.fetchall()
    except:
        response = {"Error": "General SQL error"}
        cursor.close()
        connection.close()
        return jsonify(response), 505
    cursor.close()
    connection.close()
    if toJson:
        return jsonify(response), 200
    else:
        return response

def update_data(query, data):
    connection = ""
    try:
        connection = get_db_connection()
    except:
        response = {"Error": "Unable to connect to the database"}
        return jsonify(response), 505
    try:
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, data)
        connection.commit()
    except:
        response = {"Error": "General SQL error"}
        cursor.close()
        connection.close()
        return jsonify(response), 505
    cursor.close()
    connection.close()
    response = {"Success": "Database updated"}
    return jsonify(response), 200


@app.route('/notes', methods=['GET'])
def notes():
    data = get_data("""SELECT * from note;""", (None), True)
    return data

@app.route('/note/<note_id>', methods=['GET', 'DELETE'])
def note(note_id):
    if request.method == 'GET':
        data = get_data("""SELECT * from note WHERE note_id='%s';""", (AsIs(note_id),), True)
        return data
    if request.method == 'DELETE':
        data = update_data("""DELETE from note WHERE note.note_id=%s;""", (AsIs(note_id),))
        return data

@app.route('/newnote', methods=['POST'])
def new_note():
    req_data = request.get_json()
    palace_id = int(req_data['palace_id'])
    note_title = req_data['note_title']
    note_description = req_data['note_description']
    note_location_x = req_data['note_location_x']
    note_location_y = req_data['note_location_y']
    note_image_url = req_data['note_image_url']
    note_status = req_data['note_status']
    response = update_data("""INSERT INTO note (palace_id,note_title,note_description,note_location_x,note_location_y,note_image_url,note_status) VALUES (%s, %s, %s, %s, %s, %s, %s);""", (palace_id,note_title,note_description,note_location_x,note_location_y,note_image_url,note_status))
    return response

@app.route('/updatenotestatus/<note_id>', methods=['POST'])
def update_note_status(note_id):
    args = request.args
    note_status = args['status']
    status = True if (note_status == "true") else False
    response = update_data("""UPDATE note SET note_status='%s' WHERE note_id='%s';""", (AsIs(status), AsIs(note_id)))
    return response

@app.route('/users', methods=['GET'])
def users():
    data = get_data("""SELECT * from users;""", (None), True)
    return data

@app.route('/user/<user_id>', methods=['GET', 'DELETE'])
def user(user_id):
    if request.method == 'GET':
        data = get_data("""SELECT * from users WHERE user_id=%s;""", (AsIs(user_id),), True)
        return data
    if request.method == 'DELETE':
        data = update_data("""DELETE from users WHERE users.user_id=%s;""", (AsIs(user_id),))
        return data

@app.route('/userbyusername/<user_username>', methods=['GET', 'DELETE'])
def user_by_username(user_username):
    if request.method == 'GET':
        data = get_data("""SELECT * from users WHERE user_username='%s';""", (AsIs(user_username),), True)
        return data
    if request.method == 'DELETE':
        data = update_data("""DELETE from users WHERE users.user_username='%s';""", (AsIs(user_username),))
        return data

@app.route('/newuser', methods=['POST'])
def new_user():
    req_data = request.get_json()
    user_name = req_data['user_name']
    user_username = req_data['user_username']
    user_password = req_data['user_password']
    response = update_data("""INSERT INTO users (user_name, user_username, user_password) VALUES (%s, %s, %s);""", (user_name, user_username, user_password))
    return response


@app.route('/palaces', methods=['GET'])
def palaces():
    data = get_data("""SELECT * from palace""", (None), True)
    return data

@app.route('/palacesbyuser', methods=['GET'])
def palacesbyuser():
    args = request.args
    username = args['user']
    data = get_data("""SELECT * from palace WHERE user_id=(SELECT user_id from users WHERE user_username='%s');""", (AsIs(username),), True)
    return data

@app.route('/palace/<palace_id>', methods=['GET', 'DELETE'])
def palace(palace_id):
    if request.method == 'GET':
        data = get_data("""SELECT * from palace WHERE palace_id='%s';""", (AsIs(palace_id),), True)
        return data
    if request.method == 'DELETE':
        data = update_data("""DELETE FROM palace WHERE palace.palace_id='%s';""", (AsIs(palace_id),))
        return data

@app.route('/newpalace', methods=['POST'])
def new_palace():
    req_data = request.get_json()
    user_username = req_data['user_username']
    palace_title = req_data['palace_title']
    palace_description = req_data['palace_description']
    data = get_data("""SELECT user_id from users WHERE user_username='%s';""", (AsIs(user_username),), False)
    user_id = []
    for elem in data:
        user_id.append(int(elem['user_id']))
    response = update_data("""INSERT INTO palace (user_id,palace_title,palace_description) VALUES (%s, %s, %s);""", (user_id[0],palace_title,palace_description))
    return response

@app.route('/unrememberednotes', methods=['GET'])
def unremembered_notes():
    args = request.args
    title = args['ptitle']
    username = args['user']
    data = get_data("""SELECT * from note WHERE note_status=false AND palace_id=(SELECT palace_id from palace WHERE palace_title='%s' AND user_id=(SELECT user_id from users WHERE user_username='%s'));""", (AsIs(title),AsIs(username)), True)
    return data

@app.route('/progress', methods=['GET'])
def progress():
    args = request.args
    title = args['ptitle']
    username = args['user']
    all_notes = get_data("""SELECT COUNT(note_id) from note WHERE palace_id=(SELECT palace_id from palace WHERE palace_title='%s' AND user_id=(SELECT user_id from users WHERE user_username='%s'));""", (AsIs(title),AsIs(username)), False)
    print(all_notes)
    total = []
    for elem in all_notes:
        total.append(int(elem['count']))
    remembered_notes = get_data("""SELECT COUNT(note_id) from note WHERE note_status=true AND palace_id=(SELECT palace_id from palace WHERE palace_title='%s' AND user_id=(SELECT user_id from users WHERE user_username='%s'));""", (AsIs(title),AsIs(username)), False)
    remembered = []
    for elem in remembered_notes:
        remembered.append(int(elem['count']))
    response = {}
    response['remembered'] = remembered[0]
    response['total'] = total[0]
    return jsonify(response)

@app.route('/nearestnote/<palace_id>', methods=['GET'])
def nearest_note(palace_id):
    args = request.args
    xpos = float(args['xpos'])
    ypos = float(args['ypos'])
    radius = float(args['rad'])
    if xpos is None or ypos is None or radius is None:
        return {"Error":"Incorrect location format passed in URL"}, 500

    data = get_data("""SELECT note_location_x, note_location_y from note WHERE palace_id='%s';""", (AsIs(palace_id),), False)
    all_locs = []
    for elem in data:
        all_locs.append((float(elem['note_location_x']), float(elem['note_location_y'])))

    cur_loc = (xpos, ypos)
    closest_loc = closest_point(cur_loc, all_locs)
    within_rad = pow(closest_loc[0] - cur_loc[0],2) + pow(closest_loc[1] - cur_loc[1],2) <= pow(radius,2)

    if within_rad:
        data = get_data("""SELECT * from note WHERE palace_id='%s' AND note_location_x='%s' AND note_location_y='%s';""", (AsIs(palace_id), AsIs(closest_loc[0]), AsIs(closest_loc[1])), True)
        return data
    else:
        response = [{"Message": "No notes within radius!"}]
        return json.dumps(response), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)