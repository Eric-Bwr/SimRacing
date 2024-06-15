from Arduino import *
from Telemetry import *
import time
import threading
from streamlit.runtime.scriptrunner import add_script_run_ctx


@st.cache_resource
def init():
    sharedData = getSharedData()

    sharedData[KEY_CSS] = open(".streamlit/style.css", "r").read()

    updateArduinoThread = threading.Thread(target=runArduino, args=(sharedData,))
    updateArduinoThread.daemon = True
    add_script_run_ctx(updateArduinoThread)
    updateArduinoThread.start()

    updateThread = threading.Thread(target=updateTelemetryData, args=(sharedData,))
    updateThread.daemon = True
    add_script_run_ctx(updateThread)
    updateThread.start()

    return sharedData


def getRPMColor(rpm):
    if rpm < 0.8:
        return rgbToHex(0, 255, 0)
    else:
        t = (rpm - 0.8) / 0.2
        r = lerp(0, 255, t)
        g = lerp(255, 0, t)
        b = 0
        return rgbToHex(r, g, b)


def renderEngineRPM(rpm, element):
    barHtml = f"""
    <div class="progress-container">
      <div class="progress-bar" id="progress-bar"/div>
    </div>
    <style>
      .progress-bar {{
        width: {rpm * 100.0}%;
        background-color: {getRPMColor(rpm)};
      }}
    </style>
    """
    element.markdown(barHtml, unsafe_allow_html=True)


def renderGear(gear, element):
    gearHtml = f"""
    <div class="gear-display">{gear}</div>
    """
    element.markdown(gearHtml, unsafe_allow_html=True)


def renderSpeed(speed, element):
    gearHtml = f"""
    <div class="speed-display">{speed}</div>
    """
    element.markdown(gearHtml, unsafe_allow_html=True)


def main():
    print("Init", flush=True)
    st.set_page_config(layout="wide")
    sharedData = init()
    st.markdown(f"""<style>{sharedData[KEY_CSS]}</style>""", unsafe_allow_html=True)

    speedDisplay = st.empty()
    gearDisplay = st.empty()
    rpmDisplay = st.empty()

    while True:
        if sharedData[KEY_IS_RACE_ON]:
            renderSpeed(f"{int(sharedData[KEY_SPEED]):03d}", speedDisplay)
            renderGear(sharedData[KEY_GEAR], gearDisplay)
            renderEngineRPM(sharedData[KEY_ENGINE_RPM_PERC], rpmDisplay)
        else:
            renderSpeed("-", speedDisplay)
            renderGear("-", gearDisplay)
            renderEngineRPM(0.0, rpmDisplay)
        time.sleep(0.02)


if __name__ == "__main__":
    main()
