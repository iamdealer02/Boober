import requests

class GoogleGeocodingClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/geocode/json"

    def geocode(self, address):
        params = {"key": self.api_key, "address": address}
        response = requests.get(self.base_url, params=params)
        data = response.json()
        print(data)
        # Extract latitude and longitude
        location = data['results'][0]['geometry']['location']
        latitude = location['lat']
        longitude = location['lng']

        return(f'Latitude: {latitude}, Longitude: {longitude}')
       
