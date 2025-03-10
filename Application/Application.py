import threading
import time
from flask import Flask, render_template
from flask_socketio import SocketIO
from Telemetry import updateTelemetryData
from Arduino import initArduino, setArduinoValues

app = Flask(__name__)
socketio = SocketIO(app)

RPM_FLASHING = 85


class Application:
    def __init__(self):
        self.running = True
        self.isRaceOn = False
        self.speed = 0.0
        self.gear = "N"
        self.rpm = 0.0

        self.telemetryThread = threading.Thread(target=updateTelemetryData, args=(self.updateTelemetryCb,), daemon=True)
        self.telemetryThread.start()
        self.arduinoThread = threading.Thread(target=self.updateArduino, daemon=True)
        self.arduinoThread.start()

    def start(self):
        while self.running:
            if self.isRaceOn:
                socketio.emit('update', {
                    'speed': int(self.speed),
                    'gear': self.gear,
                    'rpm': self.rpm,
                    'flashing': self.rpm > RPM_FLASHING
                })
            else:
                socketio.emit('update', {
                    'speed': 0,
                    'gear': "N",
                    'rpm': 0,
                    'flashing': False
                })
            time.sleep(0.01)

    def updateArduino(self):
        initArduino()
        while self.running:
            rpm = self.rpm
            if rpm < 25:
                rpm = 0
            setArduinoValues(self.speed, rpm)
            time.sleep(0.1)

    def updateTelemetryCb(self, isRaceOn, speed, gearString, rpmNorm):
        self.isRaceOn = isRaceOn
        self.speed = speed
        self.gear = gearString
        self.rpm = rpmNorm * 100.0

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
