import json
import pyrebase


def connect_to_firebase_db():
    with open("config.json", "r") as config_file:
        db_config = json.load(config_file)
    firebase = pyrebase.initialize_app(db_config)
    return firebase.database()


def write_to_db(db, uID, map_name):
    data = {map_name: {"players": [{"x": 0, "y": 0}]}}
    db.child("maps").child(uID).set(data)
