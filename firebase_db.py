import json
import pyrebase


def connect_to_firebase_db():
    with open("config.json", "r") as config_file:
        db_config = json.load(config_file)
    firebase = pyrebase.initialize_app(db_config)
    return firebase.database()


def write_to_db(db, map_uuid, map_name, map_url, char_names, char_icon_urls):
    data = {
        map_name: {
            "players": {
                idx: {"name": p_name, "icon": p_icon, "x": 0, "y": 0}
                for idx, (p_name, p_icon) in enumerate(zip(char_names, char_icon_urls))
            },
            "map_url": map_url,
        }
    }
    db.child("maps").child(map_uuid).set(data)
