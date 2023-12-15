from flask import Blueprint,  request, jsonify
from Class.map.classes import GoogleGeocodingClient
from flask_jwt_extended import jwt_required

map_bp = Blueprint("map", __name__, template_folder="templates")


google_geocoding_client = GoogleGeocodingClient(api_key="AIzaSyDs2tOOseqqVxI6Rp_ulXqja4VcsKbiuZc")

@map_bp.route("/geocode")
@jwt_required()
def geocode():
    pickup = request.form.get('Pickup')
    dropoff = request.form.get('Dropoff')

    # Perform geocoding using the Google Maps geocoding client
    geocoding_results_pickup = google_geocoding_client.geocode(address=pickup)
    geocoding_results_dropoff = google_geocoding_client.geocode(address=dropoff)

    response_data = {
        'pickup': geocoding_results_pickup,
        'dropoff': geocoding_results_dropoff
    }

    return jsonify(response_data)
