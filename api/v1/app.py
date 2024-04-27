#!/usr/bin/python3
""" Main module of an API!"""
from flask import Flask, Blueprint, jsonify
from models import storage
from api.v1.views import app_views
from os import environ

app = Flask(__name__)
app.register_blueprint(app_views)


@app.errorhandler(404)
def err_not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def stop(error):
    """ Closes the db storage. """
    storage.close()


if __name__ == "__main__":
    host = environ.get('HBNB_API_HOST')
    port = environ.get('HBNB_API_PORT')
    if not host:
        host = '0.0.0.0'
    if not port:
        port = '5000'
    app.run(host, port, threaded=True)
