from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
clients = {}
positions = {}
colors = ["green", "blue", "red", "yellow", "purple", "orange", "pink", "cyan"]
available_colors = colors.copy()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    global available_colors
    client_id = request.sid

    if not available_colors:
        available_colors = colors.copy()
    client_color = random.choice(available_colors)
    available_colors.remove(client_color)

    positions[client_id] = {"x": random.randint(0, 750), "y": random.randint(0, 550), "color": client_color}
    clients[client_id] = client_color

    emit('init', {'color': client_color, 'id': client_id})
    emit('update_positions', positions, broadcast=True)

@socketio.on('move')
def handle_move(data):
    client_id = request.sid
    if client_id in positions:
        positions[client_id]['x'] += data['x']
        positions[client_id]['y'] += data['y']
        emit('update_positions', positions, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    if client_id in positions:
        client_color = positions[client_id]['color']
        available_colors.append(client_color)
        del positions[client_id]
        del clients[client_id]
        emit('update_positions', positions, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True, allow_unsafe_werkzeug=True)