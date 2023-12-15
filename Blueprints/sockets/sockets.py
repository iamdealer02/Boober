from flask import Blueprint
from flask_login import current_user
from flask_socketio import SocketIO, emit
from Database.MongoDB.driver import get_vehicle_type

sockets_bp = Blueprint("sockets", __name__, template_folder="templates")
socketio = SocketIO()


@socketio.on('connect', namespace='/sockets')
# this event will be called in two frontend files : clients and driver_workspace
def handle_connect():
    if current_user.role == 'driver':
        # if the current user is a driver I make them join a specific room to broadcast ride request message
        vehicle_type = get_vehicle_type(current_user.id)
        room_name = f'driver_{vehicle_type}'
        join_room(room_name)
        emit('message', {'data': f'Connected as driver, ', 'room': room_name})
    # the clients are connected here and emits the data to the frontend
    print('Client connected')
    emit('message', {'data': 'Client Connected'},broadcast=True)


# @socketio.on('ride_request', namespace='/sockets')
# # this event will recieve all the ride requests from the clients and send this to drivers
# def handle_ride_request():
#     # initialising the ride data as a list of all the not accepted rides
#     ride_data = []
#     # getting the list of all the not accepted rides    

