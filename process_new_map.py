import os
import subprocess
import sys
import urllib.request
import uuid
from pathlib import Path
from shutil import copyfile
from urllib.parse import quote

from firebase_db import connect_to_firebase_db, write_to_db


MAPS_PATH = "./static/"


def download_map_base_image(map_UUID, map_name, map_extension, map_url):
    Path(os.path.join(MAPS_PATH, map_UUID)).mkdir(parents=True, exist_ok=True)
    map_image_file = os.path.join(MAPS_PATH, map_UUID, f"{map_name}.{map_extension}")
    urllib.request.urlretrieve(map_url, map_image_file)
    return map_image_file


def create_tiles(map_UUID, map_name, map_extension, map_image_file):
    tile_path = os.path.join(MAPS_PATH, map_UUID, 'tiles')
    subprocess.run(
        ["vips", "dzsave", "--layout", "google", map_image_file, tile_path,]
    )
    # Count number of zooms available
    number_zooms = len(
        [
            name
            for name in os.listdir(tile_path)
            if os.path.isdir(os.path.join(tile_path, name))
        ]
    )
    return number_zooms


def get_characters(form):
    char_names = [
        char["char_name"] for char in form.data["characters"] if char["char_name"] != ""
    ]
    char_icon_urls = [
        char["char_url"] for char in form.data["characters"] if char["char_url"] != ""
    ]
    return char_names, char_icon_urls


def create_map_from_form(form):
    # Create unique ID
    map_UUID = str(uuid.uuid4())

    # Grab map info
    map_name = quote(form.map_name.data)
    map_base_url = form.map_base_url.data
    map_extension = map_base_url.split(".")[-1]

    # Grab character info
    char_names, char_icon_urls = get_characters(form)

    # Download base image and make tiles
    map_image_file = download_map_base_image(
        map_UUID, map_name, map_extension, map_base_url
    )
    number_zooms = create_tiles(map_UUID, map_name, map_extension, map_image_file)

    # Hardcode the number of available zooms in the UUID
    map_image_path = map_image_file.rsplit("/", 1)[0]
    os.rename(map_image_path, map_image_path+f"-{number_zooms}")
    map_UUID += f"-{number_zooms}"

    # Update database
    db = connect_to_firebase_db()
    write_to_db(db, map_UUID, map_name, map_base_url, char_names, char_icon_urls)

    # Create map website
    map_website_path = os.path.join(map_UUID, map_name + ".html")
    map_website_path = "Your map file is: maps/" + map_website_path
    return map_website_path
