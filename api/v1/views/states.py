#!/usr/bin/python3
""" The index of the app."""
from flask import Flask, jsonify
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


