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
        while self.running:
            socketio.emit('updateCoordinates', {
                'lat': self.latitude,
                'lon': self.longitude,
                'alt': self.altitude,
                'status': self.status,
                'closestDistance': self.closestDistance
            })
            time.sleep(0.1)

    def stop(self):
        self.running = False
        self.sock.close()


application = Application()


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    application = threading.Thread(target=application.start, daemon=True)
    application.start()

    socketio.run(app, host='0.0.0.0', port=8501, allow_unsafe_werkzeug=True)
