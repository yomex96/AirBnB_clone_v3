#!/usr/bin/python3
"""connect the API with the database"""
from api.v1.views import app_views
from flask import jsonify
from models import storage

stats_list = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status')
def api_status():
    """

    """
    response = {'status': "OK"}
    return jsonify(response)
