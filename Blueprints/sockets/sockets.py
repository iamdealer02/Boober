from flask import Blueprint
from flask_login import current_user
from flask_socketio import SocketIO, emit,join_room
from Database.MongoDB.driver import get_vehicle_type

sockets_bp = Blueprint("sockets", __name__, template_folder="templates")
socketio = SocketIO()


@socketio.on('connect', namespace='/sockets')
# this event will be called in two frontend files : clients and driver_workspace
def handle_connect():
    print(current_user.role)
    if current_user.role == 'driver':
        # if the current user is a driver I make them join a specific room to broadcast ride request message
        print('driver')
        vehicle_type = get_vehicle_type(current_user.id)
        room_name = f'driver_{vehicle_type}'
        print('DRIVER ROOM NAME :', room_name)
        join_room(room_name)
        emit('message', {'data': f'Connected as driver ', 'room': room_name})
    
    # the clients are connected here and emits the data to the frontend
    else:
        print('Client connected')
        emit('message', {'data': 'Client Connected'},broadcast=True)


@socketio.on('ride_request', namespace='/sockets')
# this event will recieve all the ride requests from the clients and send this to drivers
def handle_ride_request(data):
    # getting the room name and the ride message from the client
    room_name = data.get('room_name', None)
    message = data.get('message', None)
    message['client_id'] = current_user.id
    print(room_name, message)
    print('role : ',current_user.role)
    if room_name and message :
        print('Emitting message to room:', room_name)
        # sending the message to everyone in the room 
        socketio.emit('receive_ride_message', {'message': message}, room=room_name, namespace='/sockets')

@socketio.on('ride_accepted', namespace="/sockets")
# delete the message in the drivers room when some driver accepts the ride
def handle_accepted_ride(ride_id):
    message = {'ride_id': ride_id['ride_id'], 'status': 'Accepted'}
    vehicle_type = get_vehicle_type(current_user.id)
    room_name = f'driver_{vehicle_type}'
    socketio.emit('ride_accepted', {'message': message}, room=room_name, namespace='/sockets')
