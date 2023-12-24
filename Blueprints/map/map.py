from flask import Blueprint,  request, jsonify
from Class.map.classes import GoogleGeocodingClient
from Helpers.Price.price import distance, calculate_price
import os

map_bp = Blueprint("map", __name__, template_folder="templates")


google_geocoding_client = GoogleGeocodingClient(api_key=os.getenv("MAP_API_KEY"))

@map_bp.route("/geocode", methods=['POST'])
def geocode():
  
    pickup = request.form.get('Pickup')
    dropoff = request.form.get('Dropoff')
    print('geocoding')
    # Perform geocoding using the Google Maps geocoding client
    geocoding_results_pickup = google_geocoding_client.geocode(address=pickup)
    geocoding_results_dropoff = google_geocoding_client.geocode(address=dropoff)

    response_data = {
        'pickup': geocoding_results_pickup,
        'dropoff': geocoding_results_dropoff
    }
 
    print(response_data)
    pickup_latitude, pickup_longitude = extract_coordinates(geocoding_results_pickup)
    dropoff_latitude, dropoff_longitude = extract_coordinates(geocoding_results_dropoff)
    calculated_distance = distance((pickup_latitude, pickup_longitude), (dropoff_latitude, dropoff_longitude))
    price = calculate_price(calculated_distance)
    return jsonify(price)


def extract_coordinates(geocoding_result):
    # Assuming the geocoding_result is in the format 'Latitude: xx, Longitude: yy'
    if 'Latitude' in geocoding_result and 'Longitude' in geocoding_result:
        lat_str, lng_str = geocoding_result.split(', ')
        lat = float(lat_str.split(': ')[1])
        lng = float(lng_str.split(': ')[1])
        return lat, lng
    return None