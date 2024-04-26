#!/usr/bin/python3
"""view for 'User' objects that handles all default RESTFul API"""


from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_my_users():
    """retrieves the list of all 'User' objects"""
    users = storage.all(User)
    res = []
    for user in users.values():
        res.append(user.to_dict())
    return jsonify(res)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_by_id(user_id):
    """retrieve a 'User' object by it's id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    """returns an empty dictionary with the status code 200
       if the <user_id> is not linked to any 'User', raise a 404 error"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_new_user():
    """creates a 'User' object"""
    cnt = request.get_json()
    if (not cnt):
        abort(400, 'Not a JSON')
    if ('email' not in cnt):
        abort(400, 'Missing email')
    if ('password' not in cnt):
        abort(400, 'Missing password')
    user = User(**cnt)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user_by_id(user_id):
    """updates an 'User' object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if not request.get_json():
        abort(400, "Not a JSON")
    for attr, value in request.get_json().items():
        if (attr not in ["id", "created_at", "updated_at"]):
            setattr(user, attr, value)
    user.save()
    return jsonify(user.to_dict())
