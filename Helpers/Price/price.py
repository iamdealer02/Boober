import math

def distance(pickup_coords, dropoff_coords):
    # calculates distance between two points
    # pickup_coords and dropoff_coords are tuples
    # returns distance in km
    # print(pickup_coords, dropoff_coords)
    # {dropoff: 'Latitude: 48.8226916, Longitude: 2.3159817', pickup: 'Latitude: 48.8162334, Longitude: 2.3681826'}
    lat1, lon1 = pickup_coords
    lat2, lon2 = dropoff_coords
    radius = 6371  # km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = radius * c
    return distance


def calculate_price(distance):
    Green = round(3.5 * distance, 2)
    MotoTaxi = round(1.5 * distance, 2)
    Taxi = round(4 * distance, 2)
    Berlin = round(2.5 * distance, 2)
    Comfort = round(5 * distance, 2)
    Van = round(4.75 * distance, 2)
    UberPet = round(5 * distance, 2)
    SpaceShip = round(100 * distance, 2)
    
    # return it as a dictionary
    return {'GreenPrice': Green, 'MotoTaxiPrice': MotoTaxi, 'TaxiPrice': Taxi, 'BerlinPrice': Berlin, 'ComfortPrice': Comfort, 'VanPrice': Van, 'UberPetPrice': UberPet, 'SpaceShipPrice': SpaceShip}
