#!/usr/bin/python3
""" The index of the app."""
from flask import Flask, jsonify
from api.v1.views import app_views



@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """ Returns the status of the api."""
    return jsonify({"status": "OK"})
