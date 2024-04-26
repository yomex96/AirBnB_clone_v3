#!/usr/bin/python3
"""index module"""

from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User
}


@app_views.route('/status')
def json_returned():
    """returns a JSON: '"status": "OK"' """
    return jsonify(status="OK")


@app_views.route('/stats')
def stats():
    """retrieves the number of each objects by type"""
    objs = {}
    for key, value in classes.items():
        objs[key] = storage.count(value)
    return jsonify(objs)
