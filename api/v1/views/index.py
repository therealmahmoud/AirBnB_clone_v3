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


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ Returns the status of the api."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_num():
    """ Retrieves the number of each objects by type."""
    dic = {}
    classes = [Amenity, City, Place, Review, State, User]
    name = ["amenities", "cities", "places", "reviews", "states", "users"]
    for i in range(len(classes)):
        dic[name[i]] = storage.count(classes[i])
    return jsonify(dic)
