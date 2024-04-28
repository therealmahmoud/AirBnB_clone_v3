#!/usr/bin/python3
""" objects that handles all default RestFul API actions for cities """
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/cities/<city_id>/', methods=['GET'], strict_slashes=False)
def city_get(city_id):
    """ Retrieves the list of all State objects."""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def city_id_get(state_id):
    """ Get an object."""
    clas = storage.get(State, state_id)
    if not clas:
        abort(404)
    lis = []
    for i in clas.cities:
        lis.append(i.to_dict())
    return jsonify(lis)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """ Delete an object."""
    clas = storage.get(City, city_id)
    if not clas:
        abort(404)
    storage.delete(clas)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """ Post an object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    obj = City(**data)
    obj.state_id = state.id
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """ Put or update an object."""
    clas = storage.get(City, city_id)
    if not clas:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    hash = ['id', 'state_id', 'created_at', 'updated_at']
    dct = request.get_json()
    for key, value in dct.items():
        if key not in hash:
            setattr(clas, key, value)
    storage.save()
    return make_response(jsonify(clas.to_dict()), 200)
