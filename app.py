import time
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

state = {
    'is_playing': False,
    'current_time': 0.0,
    'last_update': time.time()
}


def get_current_time():
    if state['is_playing']:
        return state['current_time'] + (time.time() - state['last_update'])
    return state['current_time']


@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('connect')
def on_connect():
    emit('sync', {
        'is_playing': state['is_playing'],
        'current_time': get_current_time()
    })


@socketio.on('play')
def on_play(data):
    state['is_playing'] = True
    state['current_time'] = data.get('current_time', 0.0)
    state['last_update'] = time.time()
    emit('play', {'current_time': state['current_time']}, broadcast=True, include_self=False)


@socketio.on('pause')
def on_pause(data):
    state['is_playing'] = False
    state['current_time'] = data.get('current_time', 0.0)
    state['last_update'] = time.time()
    emit('pause', {'current_time': state['current_time']}, broadcast=True, include_self=False)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000,
                 allow_unsafe_werkzeug=True)
