'''
Basic Websocket signaling server.
Acting as a relay for SDP and ICE candidates between two clients.

My use case only requires two, but this can be extended by using rooms.
'''

from flask import Flask, render_template, render_template_string
from flask_socketio import SocketIO
from flask_cors import CORS

PORT = 8080
app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins='*')

# Serve index to show server is running
@app.route('/')
def index():
    return render_template_string('Websocket server is running')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('offer')
def handle_offer(data):
    print('Relaying offer')
    socketio.emit('offer', data, include_self=False)

@socketio.on('answer')
def handle_answer(data):
    print('Relaying answer')
    socketio.emit('answer', data,  include_self=False)

@socketio.on('ice_candidate')
def handle_ice_candidate(data):
    print('Relaying ICE candidate')
    socketio.emit('ice_candidate', data, include_self=False)

if __name__ == '__main__':
    print(f'Running on http://0.0.0.0:{PORT}')
    socketio.run(app, host='0.0.0.0', port=PORT)