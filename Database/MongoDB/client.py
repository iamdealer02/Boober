from pymongo import MongoClient
from datetime import datetime
from gridfs import GridFS
from bson import ObjectId
from io import BytesIO 
# Create a new client and connect to the server
client = MongoClient("mongodb://localhost:27017")



db = client['Uber']
collection = db['client']
fs = GridFS(db)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

def add_client_name(sql_id, name):
    # Check if the client with the given sql_id already exists
    existing_client = collection.find_one({'sql_id': sql_id})

    if existing_client:
        # If the client exists, update their name
        collection.update_one({'sql_id': sql_id}, {'$set': {'name': name}})
        return {'success': True, 'message': 'Name updated successfully'}
    else:
        # If the client doesn't exist, create a new client with the given name
        new_client = {'sql_id': sql_id, 'name': name}
        collection.insert_one(new_client)
        return {'success': True, 'message': 'Client created successfully with the given name'}

def add_client_email(sql_id, email):
    # Check if the client with the given sql_id already exists
    existing_client = collection.find_one({'sql_id': sql_id})

    if existing_client:
        # If the client exists, update their email
        collection.update_one({'sql_id': sql_id}, {'$set': {'email': email}})
        return {'success': True, 'message': 'Email updated successfully'}
    else:
        # If the client doesn't exist, create a new client with the given email
        new_client = {'sql_id': sql_id, 'email': email}
        collection.insert_one(new_client)
        return {'success': True, 'message': 'Client created successfully with the given email'}

def add_client_address(sql_id, address):
    # Check if the client with the given sql_id already exists
    existing_client = collection.find_one({'sql_id': sql_id})

    if existing_client:
        # If the client exists, update their address
        collection.update_one({'sql_id': sql_id}, {'$set': {'address': address}})
        return {'success': True, 'message': 'Address updated successfully'}
    else:
        # If the client doesn't exist, create a new client with the given address
        new_client = {'sql_id': sql_id, 'address': address}
        collection.insert_one(new_client)
        return {'success': True, 'message': 'Client created successfully with the given address'}
def get_client_info(sql_id):
    # Query the database to find the client with the given SQL ID
    client_info = collection.find_one({'sql_id': sql_id})

    if client_info:
        # If the client is found, return their information
        return client_info
    else:
        # If the client is not found, return None
        return None
