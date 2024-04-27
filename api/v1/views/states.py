#!/usr/bin/python3
""" The index of the app."""
from flask import Flask, jsonify, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states_get():
	return storage.all(State)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states_id_get(id):
	clas = storage.get(State, id)
	if clas is None:
		raise 404
	return clas


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def del_states():
	clas = storage.get(State, id)
	if clas is None:
		raise 404
	storage.delete(clas)
	return {}


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_States():
	dct = request.get_json()
	if type(dct) != dict:
		raise 400("Not a JSON")
	if not dct["name"]:
		raise 400("Missing name")
	storage.new(dct)
	storage.get(State,dct["id"])


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_states(id):
	clas = storage.get(State, id)
	if clas is None:
		raise 404
	dct = request.get_json()
	if type(dct) != dict:
		raise 400("Not a JSON")
	for key, Value in dct.items():
		if key is "id":
			continue
		if key is "created_at":
			continue
		if key is "updated_at":
			continue
		clas[key] = Value
	storage.new(dct)
	storage.get(State,dct["id"])
	