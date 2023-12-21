from flask import Blueprint, session
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
        if session['driver_satus']:
                room_name = session['ride_id']
                print('Client_room_name is : ', room_name)
                join_room(room_name)
                socketio.emit('Driver_message', {'data': 'Client Connected'},room=room_name)
        # if the current user is a driver I make them join a specific room to broadcast ride request message
        else:
            vehicle_type = get_vehicle_type(current_user.id)
            room_name = f'driver_{vehicle_type}'
            join_room(room_name)
            emit('message', {'data': f'Connected as driver ', 'room': room_name})
    
@socketio.on('connectClient', namespace='/sockets')
def handle_connect_client(ride_id):
    room_name = ride_id['ride_id']
    print('Client_room_name is : ', room_name)
    join_room(room_name)
    socketio.emit('Client_message', {'data': 'Client Connected'},room=room_name)



@socketio.on('ride_request', namespace='/sockets')
# this event will recieve all the ride requests from the clients and send this to drivers
def handle_ride_request(data):
    # getting the room name and the ride message from the client
    room_name = data.get('room_name', None)
    message = data.get('message', None)
    message['client_id'] = current_user.id
    print(room_name, message)
    if room_name and message :
        print('Emitting message to room:', room_name)
        # sending the message to everyone in the room 
        socketio.emit('receive_ride_message', {'message': message}, room=room_name, namespace='/sockets')

@socketio.on('ride_accepted', namespace="/sockets")
# delete the message in the drivers room when some driver accepts the ride
def handle_accepted_ride(ride_id):
    message = {'ride_id': ride_id['ride_id'], 'status': 'Accepted'}
    session['driver_satus'] = 'busy'
    vehicle_type = get_vehicle_type(current_user.id)
    room_name = f'driver_{vehicle_type}'
    socketio.emit('ride_accepted', {'message': message}, room=room_name, namespace='/sockets')

    client_room_name = ride_id['ride_id']
    socketio.emit('ride_accepted_client', {'message': message}, room=client_room_name, namespace='/sockets')



@socketio.on('ride_started', namespace="/sockets")
def handle_ride(ride_id):
    # join the client and the driver here 
    # the driver will join the client room and the client will be redirected 
        room_name = ride_id['ride_id']
        print('Driver is connected to client ',room_name)
        join_room(room_name)
        socketio.emit('Driver_message', {'data': 'Driver Connected'},room=room_name)
    
@socketio.on('personal_chat', namespace="/sockets")
def personal_chat(data):
    room_name = data['ride_id']
    print(f'Server: Emitting personal_chat_receiver to room {room_name}')
    message = data['message']
    sender = current_user.role
    print(message)
    emit('personal_chat_receiver', {'message': message, 'sender': sender}, room=room_name)

    