#!/usr/bin/python3
""" objects that handles all default RestFul API actions for user """
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users',
                 methods=['GET'], strict_slashes=False)
def get_user():
    """ Get an object."""
    clas = storage.all(User).values()
    lis = []
    for i in clas:
        lis.append(i.to_dict())
    return jsonify(lis)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user_id(user_id):
    """ Retrieves an user """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """ Delete an object."""
    clas = storage.get(User, user_id)
    if not clas:
        abort(404)
    storage.delete(clas)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'],
                 strict_slashes=False)
def post_user():
    """ Post an object."""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    data = request.get_json()
    obj = User(**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """ Put or update an object."""
    if not request.get_json():
        abort(400, description="Not a JSON")
    hash = ['id', 'email', 'created_at', 'updated_at']
    clas = storage.get(User, user_id)
    if not clas:
        abort(404)
    dct = request.get_json()
    for key, value in dct.items():
        if key not in hash:
            setattr(clas, key, value)
    storage.save()
    return make_response(jsonify(clas.to_dict()), 200)
