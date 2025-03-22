from flask import Blueprint, jsonify, request
from services import get_city_averages, get_king_county_average, get_correlations, get_lowest_price_per_sqft, get_lowest_price_per_sqft_by_city, get_price_category_frequency, get_all_price_trends, get_price_trends_by_city
from pymongo.errors import PyMongoError

housing_bp = Blueprint("housing", __name__)

@housing_bp.route("/city_averages", methods=["GET"])
def city_averages():
    city_averages = get_city_averages()
    return jsonify(city_averages), 200

@housing_bp.route("/king_county_average", methods=["GET"]) 
def king_county_average():
    king_county_average = get_king_county_average()
    return jsonify(king_county_average), 200 

@housing_bp.route("/correlations", methods=["GET"])
def correlations():
    correlations = get_correlations()
    return jsonify(correlations), 200

@housing_bp.route("/lowest_price_per_sqft", methods=["GET"])
def lowest_price_per_sqft():
    lowest_price_per_sqft = get_lowest_price_per_sqft()
    return jsonify(lowest_price_per_sqft), 200   

@housing_bp.route("/lowest_price_per_sqft_by_city", methods=["GET"])
def lowest_price_per_sqft_by_city():
    lowest_price_per_sqft_by_city = get_lowest_price_per_sqft_by_city()
    return jsonify(lowest_price_per_sqft_by_city), 200

@housing_bp.route("/price_category_frequency", methods=["GET"])
def price_category_frequency():
    price_category_frequency = get_price_category_frequency()
    return jsonify(price_category_frequency), 200

@housing_bp.route("/price_trends", methods=["GET"])
def price_trends():
    price_trends = get_all_price_trends()
    return jsonify(price_trends), 200

@housing_bp.route("/price_trends_by_city", methods=["GET"])
def price_trends_by_city():
    city = request.args.get("city")
    price_trends_by_city = get_price_trends_by_city(city)
    return jsonify(price_trends_by_city), 200