from pymongo import MongoClient
from datetime import datetime
from gridfs import GridFS
from bson import ObjectId
from io import BytesIO 
# Create a new client and connect to the server
client = MongoClient("mongodb://localhost:27017")



db = client['Uber']
collection = db['driver']
fs = GridFS(db)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def add_driver_details(id,fname,lname, email, driveCity, vehicleType, identity, photo, kbis, license, vehicle_photo, birthCertificate):
    print("adding the driver")
    posted_at = datetime.utcnow().date().isoformat()

    # Save files to GridFS
    identity_file_id = fs.put(identity, filename='identity')
    driver_photo_id = fs.put(photo, filename='driver_photo')
    kbis_file_id = fs.put(kbis, filename='kbis')
    license_file_id = fs.put(license, filename='license')
    vehicle_photo_id = fs.put(vehicle_photo, filename='vehicle_photo')
    birth_certificate_file_id = fs.put(birthCertificate, filename='birth_certificate')

    driver = {
        'Sqlid': id,
        'Firstname': fname,
        'Lastname' : lname,
        'Email': email,
        'DriveCity': driveCity,
        'VehicleType': vehicleType,
        'Identity_file_id': identity_file_id,
        'Driver_Photo_id': driver_photo_id,
        'KBIS_File_id': kbis_file_id,
        'License_id': license_file_id,
        'Vehicle_Photo_id': vehicle_photo_id,
        'BirthCertificate_id': birth_certificate_file_id,
        'verified': 0,
        'posted_at': posted_at
    }

    print("Done")
    collection.insert_one(driver)

def is_verified(id):
    driver_record = collection.find_one({'Sqlid': id})
    if driver_record:
        verified_status = driver_record.get('verified')
        if verified_status == 0:
            return False
        elif verified_status == 1:
            return True
    else:
        print('No data found')

def verify_driver(id):
    collection.update_one({'_id': ObjectId(id)}, {'$set': {'verified': 1}})


def form_filled(id):
    return bool(collection.find_one({'Sqlid': id}))

def get_vehicle_type(id):
    driver_details = collection.find_one({'Sqlid': id})
    return driver_details['VehicleType'].split('-')[1]

def get_Driver_Pic(sql_id):
    profile= collection.find_one({'sql_id': sql_id})

    media = fs.get(ObjectId(profile['profilePic']))
    if media:
        result = BytesIO(media.read()), 'image/jpeg'
        return result
    else:
        return None

def get_driver_details(id):
    driver_details = collection.find_one({'Sqlid': id})
    if driver_details == None:
        driver_details = collection.find_one({'_id': ObjectId(id)})
    
    if driver_details:
        return driver_details
    else:

        return None
        
def add_driver_fname(sql_id, fname):
    # Check if the client with the given sql_id already exists
    existing_client = collection.find_one({'Sqlid': sql_id})

    if existing_client:
        # If the client exists, update their name
        collection.update_one({'Sqlid': sql_id}, {'$set': {'Firstname': fname}})
        return {'success': True, 'message': 'Name updated successfully'}
    else:
        # If the client doesn't exist, create a new client with the given name
        new_client = {'Sqlid': sql_id,'Firstname': fname}
        collection.insert_one(new_client)
        return {'success': True, 'message': 'Client created successfully with the given name'}
    
def add_driver_lname(sql_id, lname):
    # Check if the client with the given sql_id already exists
    existing_client = collection.find_one({'Sqlid': sql_id})

    if existing_client:
        # If the client exists, update their name
        collection.update_one({'Sqlid': sql_id}, {'$set': {'Lastname': lname}})
        return {'success': True, 'message': 'Name updated successfully'}
    else:
        # If the client doesn't exist, create a new client with the given name
        new_client = {'Sqlid': sql_id,'Lastname': lname}
        collection.insert_one(new_client)
        return {'success': True, 'message': 'Client created successfully with the given name'}

def add_driver_email(sql_id, email):
    # Check if the client with the given sql_id already exists
    existing_driver = collection.find_one({'Sqlid': sql_id})

    if existing_driver:
        # If the client exists, update their email
        collection.update_one({'Sqlid': sql_id}, {'$set': {'Email': email}})
        return {'success': True, 'message': 'Email updated successfully'}
    else:
        # If the client doesn't exist, create a new client with the given email
        new_client = {'Sqlid': sql_id, 'Email': email}
        collection.insert_one(new_client)
        return {'success': True, 'message': 'Client created successfully with the given email'}


def get_non_verified_drivers():
    existing_driver = collection.find({'verified': 0})
    return existing_driver

def get_media(media_id):
    media = fs.get(ObjectId(media_id))
    file_content = BytesIO(media.read())
    
    # Get the filename (assuming it already includes the extension)
    filename = media.filename

    # Determine the MIME type based on the file extension
    file_extension = filename.split('.')[-1].lower()
    mime_type = 'application/octet-stream'  # Default MIME type

    if file_extension == 'pdf':
        mime_type = 'application/pdf'
    elif file_extension in ['doc', 'docx']:
        mime_type = 'application/msword'
    elif file_extension in ['xls', 'xlsx']:
        mime_type = 'application/vnd.ms-excel'
    elif file_extension in ['png', 'jpg', 'jpeg', 'gif']:
        mime_type = 'image/jpeg'
    # Add more conditions as needed for other file types

    return file_content, mime_type, filename
