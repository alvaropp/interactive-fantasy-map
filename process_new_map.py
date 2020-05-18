import os
import subprocess
import sys
import urllib.request
import uuid
from pathlib import Path
from shutil import copyfile

from firebase_db import connect_to_firebase_db, write_to_db


MAPS_PATH = "./static/"


def download_map_base_image(map_UUID, map_name, map_extension, map_url):
    Path(os.path.join(MAPS_PATH, map_UUID)).mkdir(parents=True, exist_ok=True)
    map_image_file = os.path.join(MAPS_PATH, map_UUID, f"{map_name}.{map_extension}")
    urllib.request.urlretrieve(map_url, map_image_file)
    return map_image_file


def create_tiles(map_UUID, map_name, map_extension, map_image_file):
    subprocess.run(
        ["echo", "Even more output"], stdout=subprocess.PIPE, universal_newlines=True
    )
    subprocess.run(
        [
            "vips",
            "dzsave",
            "--layout",
            "google",
            f"{map_image_file}",
            f"{os.path.join(MAPS_PATH, map_UUID, 'tiles')}",
        ]
    )


def get_characters(form):
    char_names = [v for (k, v) in form.data.items() if "char_name" in k]
    char_icon_urls = [v for (k, v) in form.data.items() if "char_icon" in k]
    return char_names, char_icon_urls


def create_map_from_form(form):
    # Create unique ID
    map_UUID = str(uuid.uuid4())

    # Grab map info
    map_name = form.map_name.data
    map_base_url = form.map_base_url.data
    map_extension = map_base_url.split(".")[-1]

    # Grab character info
    char_names, char_icon_urls = get_characters(form)

    # Download base image and make tiles
    map_image_file = download_map_base_image(
        map_UUID, map_name, map_extension, map_base_url
    )
    create_tiles(map_UUID, map_name, map_extension, map_image_file)

    # Update database
    db = connect_to_firebase_db()
    write_to_db(db, map_UUID, map_name, map_base_url, char_names, char_icon_urls)

    # Create map website
    map_website_path = os.path.join(map_UUID, map_name + ".html")
    map_website_path = "Your map file is: " + map_website_path
    return map_website_path
