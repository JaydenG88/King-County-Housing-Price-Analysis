from flask import Blueprint, jsonify, request
from housing_data_API.services.housing_services import get_averages, get_correlations, get_lowest_price_per_sqft, get_price_category_frequency, get_price_trends

housing_bp = Blueprint("housing", __name__)

@housing_bp.route("/averages/<string:metric>/<string:type>", methods=["GET"])
def city_averages(metric, type):
    city_averages = get_averages(metric, type)
    return jsonify(city_averages), 200

@housing_bp.route("/correlations", methods=["GET"])
def correlations():
    correlations = get_correlations()
    return jsonify(correlations), 200

@housing_bp.route("/lowest_price_per_sqft/<string:region>", methods=["GET"])
def lowest_price_per_sqft(region):
    lowest_price_per_sqft = get_lowest_price_per_sqft(region)
    return jsonify(lowest_price_per_sqft), 200   

@housing_bp.route("/price_category_frequency", methods=["GET"])
def price_category_frequency():
    price_category_frequency = get_price_category_frequency()
    return jsonify(price_category_frequency), 200

@housing_bp.route("/price_trends/<string:region>/<string:metric>/<string:type>", methods=["GET"])
def price_trends(region, metric, type):
    price_trends = get_price_trends(region, metric, type)
    return jsonify(price_trends), 200
