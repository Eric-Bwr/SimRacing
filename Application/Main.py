from Arduino import *
from Telemetry import *
import time
import threading
from streamlit.runtime.scriptrunner import add_script_run_ctx


@st.cache_resource
def init():
    sharedData = getSharedData()

    updateArduinoThread = threading.Thread(target=runArduino, args=(sharedData,))
    updateArduinoThread.daemon = True
    add_script_run_ctx(updateArduinoThread)
    updateArduinoThread.start()

    updateThread = threading.Thread(target=updateTelemetryData, args=(sharedData,))
    updateThread.daemon = True
    add_script_run_ctx(updateThread)
    updateThread.start()

    return sharedData


def setBackgroundColor(color):
    css = f"""
    div[data-baseweb="progress-bar"] > div > div > div {{
        background-color: {color};
    }}
    """
    st.markdown(f"""<style>{css}</style>""", unsafe_allow_html=True)


def calcBackgroundColor(rpm):
    if rpm < 0.7:
        return "#FFFFFF"
    else:
        t = (rpm - 0.7) / 0.3
        r = lerp(0, 255, t)
        g = lerp(255, 0, t)
        b = 0
        return rgbToHex(r, g, b)


def main():
    print("Init", flush=True)
    st.set_page_config(layout="wide")
    sharedData = init()

    css = open(".streamlit/style.css", "r").read()
    st.markdown(f"""<style>{css}</style>""", unsafe_allow_html=True)

    speedDisplay = st.empty()
    gearDisplay = st.empty()
    rpm = st.progress(value=0.0)

    while True:
        if sharedData[KEY_IS_RACE_ON]:
            speedDisplay.text(f"""{format(sharedData[KEY_SPEED], ".0f")}kmh""")
            gearDisplay.text(f"""{sharedData[KEY_GEAR]}""")
            rpm.progress(sharedData[KEY_ENGINE_RPM_PERC])
            setBackgroundColor(calcBackgroundColor(sharedData[KEY_ENGINE_RPM_PERC]))
        else:
            speedDisplay.text("---")
            gearDisplay.text("---")
            rpm.progress(0.0)
            setBackgroundColor(calcBackgroundColor(0.0))
        time.sleep(0.01)


if __name__ == "__main__":
    main()
