import os
from math import sin, atan2, sqrt, cos

from flask import Flask, request, send_from_directory
import hashlib

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("config.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask('YouMadeIt')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['FLASK_ENV'] = os.environ.get('FLASK_ENV')


def hash_password(password):
    h = hashlib.md5(password.encode())
    return h.hexdigest()


@app.route("/")
def start():
    return "hello"


@app.route('/favicon.ico')
def icon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/login', methods=["POST"])
def login():
    try:
        values = request.get_json()
        if "phone" not in values or "password" not in values:
            return "402"

        existing_user = user_exist_from_values(values)

        if existing_user is None:
            return "401"

        if hash_password(values["password"]) == existing_user.get("password"):
            return existing_user.to_dict()

        return "404"
    except():
        return "404"


def user_exist_from_values(values):
    docs = db.collection(u'users').stream()
    existing_user = None
    for doc in docs:
        if doc.id == values["phone"]:
            existing_user = doc
            break
    return existing_user


@app.route('/signup', methods=["POST"])
def signup():
    values = request.get_json()
    if "phone" not in values or "name" not in values or "password" not in values:
        return "401"

    existing_user = user_exist_from_values(values)

    if existing_user:
        return "402"

    id = values["phone"]
    password = values["password"]
    hash_pass = hash_password(password)
    values["password"] = hash_pass
    del values["phone"]
    values["points"] = 0
    db.collection(u'users').document(id).set(values)

    values["phone"] = id
    return values


@app.route('/create_event', methods=["POST"])
def create_event():
    values = request.get_json()
    if "creator_phone" not in values or \
            "worker_phone" not in values or \
            "type" not in values or \
            "name" not in values or \
            "about" not in values or \
            "location_x" not in values or \
            "location_y" not in values or \
            "points" not in values or \
            "time" not in values:
        return "401"

    db.collection(u'events').document().set(values)

    return values


@app.route('/get_all_events', methods=["GET"])
def get_events():
    docs = db.collection(u'events').stream()
    dic = []
    for item in docs:
        dic.append(item.to_dict())
    return {"all_events": dic}


@app.route('/verify_location', methods=["POST"])
def verify_location():
    values = request.get_json()

    if "location_x" not in values or "location_y" not in values or "event_id" not in values:
        return "401"

    doc = db.collection(u'events').document(values["event_id"])

    if doc is None:
        return "402"

    lat1 = values["location_x"]
    lon1 = values["location_y"]
    lat2 = doc.get("location_x")
    lon2 = doc.get("location_y")

    distance = get_distance(lat1, lat2, lon1, lon2)

    if distance < 1000:
        return True
    return False


def get_distance(lat1, lat2, lon1, lon2):
    d_lon = lon2 - lon1
    d_lat = lat2 - lat1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    R = 6373.0
    return c * R


if __name__ == '__main__':
    if (app.config["FLASK_ENV"]) == "DEBUG":
        port = 1227
        app.run(debug=True, port=port)
    else:
        app.run()
