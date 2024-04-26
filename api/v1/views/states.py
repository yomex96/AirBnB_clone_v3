#!/usr/bin/python3
''' States manager '''


from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_my_states():
    """retrieves the list of all 'State' objects"""
    states = storage.all(State)
    res = []
    for state in states.values():
        res.append(state.to_dict())
    return jsonify(res)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    ''' Retrieve a state by it's id '''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """returns an empty dictionary with the status code 200
       if the <state_id> is not linked to any 'State', raise a 404 error"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_new_state():
    ''' so, you want a new one? '''
    cnt = request.get_json()
    if (not cnt):
        abort(400, 'Not a JSON')
    if ('name' not in cnt):
        abort(400, 'Missing name')
    state = State(**cnt)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state_by_id(state_id):
    """updates a'State' object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for attr, value in request.get_json().items():
        if (attr not in ["id", "created_at", "updated_at"]):
            setattr(state, attr, value)
    state.save()
    return jsonify(state.to_dict())
