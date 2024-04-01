#!/usr/bin/python3
"""City view"""
from flask import Flask
from flask import jsonify, request, abort, make_response
from models import storage
from api.v1.views import app_views
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city_state(state_id):
    """list of city"""
    state = storage.get(State, state_id)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/states/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    """Get city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict()), 'OK'


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(state_id):
    """Delete City"""
    city = storage.get(City, state_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """CREATE City"""
    data_dict = request.get_json(silent=True)
    state = storage.get(State, state_id)
    if not state:
        return abort(404)

    if not data_dict:
        abort(400, description="Not a JSON")

    if 'name' not in data_dict:
        abort(400, description="Missing name")

    city = City(**data_dict)
    city.save()
    return jsonify(city.to_dict()), 201
