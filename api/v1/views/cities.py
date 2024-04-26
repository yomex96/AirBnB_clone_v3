#!/usr/bin/python3
''' city manager '''


from flask import jsonify, abort, request, make_response
import json
from api.v1.views import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<string:state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_my_cities(state_id):
    """retrieves the list of all 'State' objects"""
    state = storage.get(State, state_id)
    if (not state):
        abort(404)
    res = []
    for city in state.cities:
        res.append(city.to_dict())
    return jsonify(res)


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city_by_id(city_id):
    ''' Retrieve a state by it's id '''
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<string:city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    """returns an empty dictionary with the status code 200
       if the <city_id> is not linked to any 'State', raise a 404 error"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/<string:state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_new_city(state_id):
    ''' so, you want a new one? '''
    state = storage.get(State, state_id)
    if (not state):
        abort(404)
    cnt = request.get_json()
    if (not cnt):
        abort(400, 'Not a JSON')
    if ('name' not in cnt):
        abort(400, 'Missing name')
    city = City(**cnt)
    city.state_id = state.id
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city_by_id(city_id):
    """updates a'State' object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for attr, value in request.get_json().items():
        if (attr not in ["id", "created_at", "updated_at"]):
            setattr(city, attr, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
