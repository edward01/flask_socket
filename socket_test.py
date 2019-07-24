from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, rooms, join_room, leave_room
from datetime import datetime
SOCKETIO_REDIS_HOST = 'localhost'
SOCKETIO_REDIS_CHANNEL = 5

app = Flask(__name__)
broker_url = 'redis://{}:6379/{}'.format(SOCKETIO_REDIS_HOST, SOCKETIO_REDIS_CHANNEL)
socketio = SocketIO(app, message_queue=broker_url, path='s.io')

@socketio.on('join')
def socketio_join_room(room):
    join_room(room)

@socketio.on('leave')
def socketio_leave_room(room):
    leave_room(room)

@socketio.on('leave_all')
def socketio_leave_all():
    for room in rooms():
        leave_room(room)

@socketio.on('connect')
def socketio_connect(*args, **kwargs):
    print('connect')


@app.route('/', methods=['GET'])
def index():
    return render_template('socket.html')

@app.route('/push', methods=['GET'])
def socket_push():
    payload = {'abc': 123, 'dt': str(datetime.now())}
    socketio.emit('event', payload, room='dev:device1', namespace='/')
    return jsonify({'status': 'pushed'})


if __name__ == '__main__':
    socketio.run(app)       
    