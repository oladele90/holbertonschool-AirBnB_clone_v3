#!/usr/bin/python3
"""states.py"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_cities(state_id=None):
    """route that gets a city obj"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route("/cities/<city_id>", methods=["DELETE", "GET", "PUT"],
                 strict_slashes=False)
def get_or_delete(city_id=None):
    """get put and delete city methods"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == "GET":
        return jsonify(city.to_dict())
    if request.method == "DELETE":
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)
    if request.method == "PUT":
        if not request.get_json():
            return make_response(jsonify({"error": "Not a JSON"}), 400)
        else:
            city_list = request.get_json()
            ignore = ["id", "created_at", "updated_at", "state_id"]
            for key, value in city_list.items():
                if key not in ignore:
                    setattr(city, key, value)
            storage.save()
            return make_response(jsonify(city.to_dict()), 200)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def make_city(state_id=None):
    """post method for city"""
    city_list = request.get_json()
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not city_list:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if "name" not in city_list.keys():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new = City(**city_list)
    storage.save()
    return make_response(jsonify(new.to_dict()), 201)
