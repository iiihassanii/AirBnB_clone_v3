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
    if state is None:
        return abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    """Get city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """Delete City"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """CREATE City"""
    if request.content_type != 'application/json':
        return jsonify({"error": "Not a JSON"}), 400
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    if not request.get_json(silent=True):
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json(silent=True)
    if 'name' not in data:
        return abort(400, 'Missing name')
    data['state_id'] = state_id

    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a city in the database"""
    if request.content_type != 'application/json':
        return jsonify({"error": "Not a JSON"}), 400
    city = storage.get(City, city_id)
    if city:
        if not request.get_json(silent=True):
            return jsonify({"error": "Not a JSON"}), 400
        data = request.get_json(silent=True)
        ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(city, key, value)
        city.save()
        return jsonify(city.to_dict()), 200
    else:
        return abort(404)
