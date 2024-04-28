#!/usr/bin/python3
""" objects that handles all default RestFul API actions for amenity """
from models.amenity import Amenity
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenity():
    """ Get an object."""
    clas = storage.all(Amenity).values()
    lis = []
    for i in clas:
        lis.append(i.to_dict())
    return jsonify(lis)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity_id(amenity_id):
    """ Retrieves the list of all State objects."""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """ Delete an object."""
    clas = storage.get(Amenity, amenity_id)
    if not clas:
        abort(404)
    storage.delete(clas)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity(amenity_id):
    """ Post an object."""
    clas = storage.get(Amenity, amenity_id)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    obj = Amenity(**data)
    obj.state_id = clas.id
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """ Put or update an object."""
    if not request.get_json():
        abort(400, description="Not a JSON")
    hash = ['id', 'created_at', 'updated_at']
    clas = storage.get(Amenity, amenity_id)
    if not clas:
        abort(404)
    dct = request.get_json()
    for key, value in dct.items():
        if key not in hash:
            setattr(clas, key, value)
    storage.save()
    return make_response(jsonify(clas.to_dict()), 200)
