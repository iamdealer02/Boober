from pymongo import MongoClient
from datetime import datetime
# from gridfs import GridFS

# Create a new client and connect to the server
client = MongoClient("mongodb://localhost:27017")



db = client['Uber']
collection = db['rides']
# fs = GridFS(db)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def add_rides(client_id, pickup_location, dropoff_location, status='Initiated'):
    # when the driver has not been assigned
    # status stays as initiated/cancelled
    posted_at = datetime.utcnow().date().isoformat()
    ride={
        'client_id': client_id,
        'pickup_location' : pickup_location,
        'dropoff_location': dropoff_location,
        'status': status,
        'made_at': posted_at
    }

def assign_driver(ride_id, pickup_location, driver_id):
    # assigns the driver to the ride and add a driver_id to the ride
    # updates the ride status to accepted
     collection.update_one({'ride_id': ride_id}, {'$set': {'driver_id': driver_id, 'status': 'Accepted'}})   
    


def update_status(status, ride_id):
    # updates the ride status
    collection.update_one({'ride_id': ride_id}, {'$set': {'status': status}})

def get_recent_rides():
    # returns the recent rides
     collection.find().sort('made_at', -1).limit(10)