#!/usr/bin/python3
""" objects that handles all default RestFul API actions for user """
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.city import City


@app_views.route('/api/v1/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def places(place_id):
    """ Retrieves an user """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/api/v1/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_place_id(city_id):
    """ Retrieves an user """
    city = storage.get(City, city_id)
    place = storage.all(Place).values()
    if not city:
        abort(404)
    lis = []
    for i in place:
        lis.append(i.to_dict())

    return jsonify(lis)


@app_views.route('/api/v1/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """ Delete an object."""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/api/v1/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """ Post an object."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")
    user = storage.get(User, request.get_json()['user_id'])
    if not user:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    obj = Place(**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/api/v1/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """ Put or update an object."""
    if not request.get_json():
        abort(400, description="Not a JSON")
    hash = ['id', 'email', 'created_at', 'updated_at']
    clas = storage.get(Place, place_id)
    if not clas:
        abort(404)
    dct = request.get_json()
    for key, value in dct.items():
        if key not in hash:
            setattr(clas, key, value)
    storage.save()
    return make_response(jsonify(clas.to_dict()), 200)
