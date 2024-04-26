#!/usr/bin/python3
"""view for 'Review' objects that handles all default RESTFul API"""


from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def all_my_reviews(place_id):
    """retrieves the list of all 'Review' objects for a given 'Place'"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    res = []
    for review in place.reviews:
        res.append(review.to_dict())
    return jsonify(res)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """retrieve a 'Review' object by it's id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """returns an empty dictionary with the status code 200
       if the <review_id> is not linked to any 'Review', raise a 404 error"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_new_review(place_id):
    """creates a 'Review' object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    cnt = request.get_json()
    if (not cnt):
        abort(400, 'Not a JSON')
    if ('user_id' not in cnt):
        abort(400, 'Missing user_id')
    user = storage.get(User, cnt['user_id'])
    if user is None:
        abort(404)
    if ('text' not in cnt):
        abort(400, 'Missing text')
    cnt['place_id'] = place_id
    review = Review(**cnt)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review_by_id(review_id):
    """updates a 'Review' object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    cnt = request.get_json()
    if (not cnt):
        abort(400, "Not a JSON")
    for attr, value in cnt.items():
        if (attr not in ["id", 'user_id', 'place_id',
                         "created_at", "updated_at"]):
            setattr(review, attr, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
