import eventlet
eventlet.monkey_patch()

import time
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

PASSWORD = 'stream123'

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
    if not session.get('authorized'):
        return redirect(url_for('login'))
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    attempts = session.get('attempts', 0)
    first_time = session.get('first_attempt_time', time.time())
    if time.time() - first_time > 600:
        attempts = 0
        first_time = time.time()
    if request.method == 'POST':
        if attempts >= 5 and time.time() - first_time <= 600:
            error = 'Too many attempts. Try again later.'
            return render_template('login.html', error=error)
        password = request.form.get('password', '')
        if password == PASSWORD:
            session['authorized'] = True
            session['attempts'] = 0
            session['first_attempt_time'] = time.time()
            return redirect(url_for('index'))
        else:
            attempts += 1
            session['attempts'] = attempts
            session['first_attempt_time'] = first_time
            error = 'Incorrect password.'
            return render_template('login.html', error=error)
    session['attempts'] = attempts
    session['first_attempt_time'] = first_time
    return render_template('login.html')


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


@socketio.on('chat message')
def on_chat_message(data):
    msg = data.get('message', '')
    emit('chat message', {'message': msg}, broadcast=True)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000,
                 allow_unsafe_werkzeug=True)
