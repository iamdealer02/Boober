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
    if driver_details:
        # photo_id = driver_details.get('Driver_Photo_id')
        # photo = get_Driver_Pic(photo_id)
        fname = driver_details.get('Firstname')
        lname = driver_details.get('Lastname')
        return [None, fname, lname]
    else:
        return [None, None, None]


