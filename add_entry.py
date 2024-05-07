#!/usr/bin/env python3
#
# -*- coding: utf-8 -*-

import json

from geopy.geocoders import Nominatim

# config
fname = "data/blast-community.geojson"


def read_json():
    with open(fname) as json_str:
        return json.load(json_str)


def write_json(data):
    """data as dictionary"""
    json_txt = json.dumps(dict(data), sort_keys=True, indent=4)

    with open(fname, "w", encoding="utf8") as file:
        file.write(json_txt)


def append_geojson(data, lon, lat, properties):
    """..."""
    data["features"].append(
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": dict(properties),
        }
    )

    return data


def get_location(place):
    """Returns latiude and longitude for a place : string"""
    geolocator = Nominatim(user_agent="blast-communitymap")
    location = geolocator.geocode(place, timeout=5)  # 5sec timeout

    if not location:
        print("[GEOMISS] No nominatim entry for " + place)
        return

    lat = location.latitude
    lon = location.longitude

    return lat, lon


def ask_details():
    """..."""
    name = input("How to name this entry (group, division or experimental facility? ")
    institution = input("Which insitution? ")
    place = input("Where are you located (address or city, country)? ")
    poc = input("Who are the contacts (comma separated)? ").split(",")
    domain = input(
        "In which science/engineering domain (e.g., laser-plasma, beam, fusion) comma separated? "
    ).split(",")
    user = input("Which BLAST codes are used (comma separated)? ").split(",")
    dev = input("Which BLAST codes are developed (comma separated)? ").split(",")

    return name, institution, place, poc, domain, user, dev


data = read_json()

name, institution, place, poc, domain, user, dev = ask_details()
lat, lon = get_location(place)
properties = {
    "name": name,
    "contacts": poc,
    "institution": institution,
    "domain": domain,
    "user-codes": user,
    "dev-codes": dev,
}
data = append_geojson(data, lon, lat, properties)

write_json(data)
