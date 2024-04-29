#!/usr/bin/python3
""" objects that handles all default RestFul API actions for review """
from models.review import Review
from models.place import Place
from models.user import User
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """ Get an object."""
    clas = storage.all(Review).values()
    place = storage.get(Review, place_id)
    if not place:
        abort(404)
    if not clas:
        abort(404)
    lis = []
    for i in clas:
        lis.append(i.to_dict())
    return jsonify(lis)


@app_views.route('/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_id(review_id):
    """ Retrieves an review """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """ Delete an object."""
    clas = storage.get(Review, review_id)
    if not clas:
        abort(404)
    storage.delete(clas)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def post_review(place_id, user_id):
    """ Post an object."""
    if not request.get_json():
        abort(400, description="Not a JSON")
    clas = storage.get(Review, place_id)
    if not clas:
        abort(404)
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    classs = storage.get(Review, user_id)
    if not classs:
        abort(404)
    if 'text' not in request.get_json():
        abort(400, description="Missing text")
    data = request.get_json()
    obj = Review(**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """ Put or update an object."""
    clas = storage.get(Review, review_id)
    if not clas:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    hash = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    dct = request.get_json()
    for key, value in dct.items():
        if key not in hash:
            setattr(clas, key, value)
    storage.save()
    return make_response(jsonify(clas.to_dict()), 200)
