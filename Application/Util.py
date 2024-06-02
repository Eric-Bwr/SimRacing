import streamlit as st

KEY_CSS = "css"
KEY_IS_RACE_ON = "raceOn"
KEY_SPEED = "speed"
KEY_GEAR = "gear"
KEY_ENGINE_RPM = "engine"
KEY_ENGINE_RPM_MAX = "engineMax"
KEY_ENGINE_RPM_PERC = "enginePerc"


@st.cache_resource
def getSharedData():
    return {
        KEY_CSS: "",
        KEY_IS_RACE_ON: False,
        KEY_SPEED: 0.0,
        KEY_GEAR: "N",
        KEY_ENGINE_RPM: 0.0,
        KEY_ENGINE_RPM_MAX: 0.0,
        KEY_ENGINE_RPM_PERC: 0.0,
    }


def lerp(a, b, t):
    return a + (b - a) * t


def rgbToHex(r, g, b):
    return f'#{int(r):02x}{int(g):02x}{int(b):02x}'


def mapValue(value, in_min, in_max, out_min, out_max):
    return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def clampValue(value, min_val, max_val):
    return min(max(value, min_val), max_val)
