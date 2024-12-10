import threading
import time
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
socketio = SocketIO(app)


class Application:
    def __init__(self):
        self.running = True

    def start(self):
        simVal = 0
        while self.running:
            socketio.emit('update', {
                'speed': int(simVal * 2),
                'gear': 0,
                'rpm': simVal,
                'flashing': simVal > 90
            })
            simVal += 0.5
            if simVal > 100:
                simVal = 0
            time.sleep(0.1)

    def stop(self):
        self.running = False


application = Application()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    application = threading.Thread(target=application.start, daemon=True)
    application.start()

    socketio.run(app, host='0.0.0.0', port=8501, allow_unsafe_werkzeug=True)
