#!/usr/bin/python3
""" The index of the app."""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.state import State
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_state.yml', methods=['GET'])
def states_get():
    """ Retrieves the list of all State objects."""
    dic = storage.all(State).values()
    lis = []
    for state in dic:
        lis.append(state.to_dict())
    return jsonify(lis)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_id_state.yml', methods=['get'])
def states_id_get(state_id):
    """ Get an object."""
    clas = storage.get(State, state_id)
    if not clas:
        abort(404)
    return jsonify(clas.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/delete_state.yml', methods=['DELETE'])
def del_states(state_id):
    """ Delete an object."""
    clas = storage.get(State, state_id)
    if not clas:
        abort(404)
    storage.delete(clas)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post_state.yml', methods=['POST'])
def post_States():
    """ Post an object."""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")
    data = request.get_json()
    obj = State(**data)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/state/put_state.yml', methods=['PUT'])
def put_states(state_id):
    """ Put or update an object."""
    clas = storage.get(State, state_id)
    if not clas:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    hash = ['id', 'created_at', 'updated_at']
    dct = request.get_json()
    for key, value in dct.items():
        if key not in hash:
            setattr(clas, key, value)
    storage.save()
    return make_response(jsonify(clas.to_dict()), 200)
