import os
from flask_pymongo import PyMongo
from flask import Flask, request, send_from_directory


app = Flask('YouMadeIt')
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['DB_NAME'] = os.environ.get('DB_NAME')
mongo = PyMongo(app)


@app.route("/", methods=["GET", "POST"])
def start():
    return "hello"


@app.route('/favicon.ico')
def icon():
    return send_from_directory(app.static_folder, 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/login')
def login():
    if "phone" not in request.form or "password" not in request.form:
        return '401'


    db = mongo.db
    collection = db["Users"]

    existing_user = collection.find_one({"phone":request.form["phone"]})

    if existing_user is None:
        return 401
    else:
        return existing_user

port = 1227
if __name__ == '__main__':
    app.run(debug=True, port=port)
