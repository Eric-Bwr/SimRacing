from Application.Arduino import runArduino
from Util import *


def main():
    sharedData = getSharedData()
    sharedData[KEY_ENGINE_RPM_PERC] = 0.0
    sharedData[KEY_SPEED] = 150
    runArduino(sharedData)


if __name__ == "__main__":
    main()
