#!/usr/bin/python3
"""view for 'Amenity' objects that handles all default RESTFul API"""


from os import getenv
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
from models import storage


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def all_place_amenities(place_id):
    """retrieves the list of all 'Amenity' objects for a given 'Place'"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids
    res = []
    for amenity in amenities:
        res.append(amenity.to_dict())
    return jsonify(res)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_place_amenity(place_id, amenity_id):
    """deletes an 'Amenity' object to a 'Place'"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids
    if amenity not in amenities:
        abort(404)
    amenities.remove(amenity)
    place.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_amenity(place_id, amenity_id):
    """Links an 'Amenity' object to a 'Place'"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        amenities = place.amenities
    else:
        amenities = place.amenity_ids
    if amenity in amenities:
        return make_response(jsonify(amenity.to_dict()), 200)
    amenities.append(amenity)
    place.save()
    return make_response(jsonify(amenity.to_dict()), 201)
