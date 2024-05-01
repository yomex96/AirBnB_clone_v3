#!/usr/bin/python3
"""view for 'Place' objects that handles all default RESTFul API"""


from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_my_places(city_id):
    """retrieves the list of all 'Place' objects"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    res = []
    for place in city.places:
        res.append(place.to_dict())
    return jsonify(res)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place_by_id(place_id):
    """retrieve a 'Place' object by it's id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    """returns an empty dictionary with the status code 200
       if the <place_id> is not linked to any 'Place', raise a 404 error"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_new_place(city_id):
    """creates a 'Place' object"""
    cnt = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if (not cnt):
        abort(400, 'Not a JSON')
    if ('user_id' not in cnt):
        abort(400, 'Missing user_id')
    user = storage.get(User, cnt['user_id'])
    if user is None:
        abort(404)
    if ('name' not in cnt):
        abort(400, 'Missing name')
    cnt['city_id'] = city_id
    place = Place(**cnt)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place_by_id(place_id):
    """updates an 'Place' object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for attr, value in request.get_json().items():
        if (attr not in ["id", "user_id", "city_id",
                         "created_at", "updated_at"]):
            setattr(place, attr, value)
    place.save()
    return jsonify(place.to_dict())
