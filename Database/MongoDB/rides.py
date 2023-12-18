from pymongo import MongoClient
from datetime import datetime
# from gridfs import GridFS
from bson import ObjectId

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
    result = collection.insert_one(ride)
    ride_id = result.inserted_id  # Get the generated _id
    
    return ride_id

def assign_driver(ride_id, driver_id):
    # assigns the driver to the ride and add a driver_id to the ride
    # updates the ride status to accepted
    ride_id = ObjectId(ride_id)
    collection.update_one(
        {'_id': ride_id},
        {'$set': {'driver_id': driver_id, 'status': 'Accepted'},
        },

    )
    return 'done'


def update_status(status, ride_id):
    # updates the ride status
    ride_id = ObjectId(ride_id)
    collection.update_one({'_id': ride_id}, {'$set': {'status': status}})

def get_recent_rides():
    # returns the recent rides
     collection.find().sort('made_at', -1).limit(10)