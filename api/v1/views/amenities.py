#!/usr/bin/python3
"""view for 'Amenity' objects that handles all default RESTFul API"""


from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def all_my_amenities():
    """retrieves the list of all 'Amenity' objects"""
    amenities = storage.all(Amenity)
    res = []
    for amenity in amenities.values():
        res.append(amenity.to_dict())
    return jsonify(res)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """retrieve an amenity object by it's id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    """returns an empty dictionary with the status code 200
       if the <amenity_id> is not linked to any 'Amenity', raise a 404 error"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_new_amenity():
    """creates an 'Amenity' object"""
    cnt = request.get_json()
    if (not cnt):
        abort(400, 'Not a JSON')
    if ('name' not in cnt):
        abort(400, 'Missing name')
    amenity = Amenity(**cnt)
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity_by_id(amenity_id):
    """updates an 'Amenity' object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for attr, value in request.get_json().items():
        if (attr not in ["id", "created_at", "updated_at"]):
            setattr(amenity, attr, value)
    amenity.save()
    return jsonify(amenity.to_dict())
