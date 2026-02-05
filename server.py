# radhe radhe
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import logging
import main_game

app = Flask(__name__)
app.config['SECRET_KEY'] = "so-this-is-a-secret-huh!"  # Change this to a random secret key
socketio = SocketIO(app, cors_allowed_origins="*")

# Silence Flask's default request logs
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)  # Only show errors, not GET/POST requests

# Route
@app.route('/')
def index():
    return render_template('index.html')

# WebSocket logic
@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')

@socketio.on('move_piece_socket')
def handle_move_piece_socket(data):
    print(f'Received from client: {data}')

    ACN = f"{data['piece'][0]} {data['piece'][1]} {data['from']} {data['to']}"

    move_res = main_game.move(ACN)
    
    # Reply back to client
    emit('move_piece_socket', {
        'message': 'Updated Board',
        'status': move_res.get("status"),
    })

@socketio.on('disconnect')
def handle_disconnect():
    print(f'Client disconnected: {request.sid}')

# Start server
if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=3000, debug=True)  # Disable reloader to prevent duplicate logs