import usb.core
import usb.util
import uinput
import time

events = (
    uinput.BTN_A,
    uinput.BTN_B,
    uinput.ABS_X + (-32768, 32767, 0, 0),
    uinput.ABS_Y + (-32768, 32767, 0, 0),
)

device = uinput.Device(events, name="Xbox 360 Controller", vendor=0x045e, product=0x028e)

device.emit(uinput.BTN_A, 0)
device.emit(uinput.BTN_B, 0)
device.emit(uinput.ABS_X, 0)
device.emit(uinput.ABS_Y, 0)

dev = usb.core.find(idVendor=0x046d, idProduct=0xc219)
if dev is None:
    raise ValueError("Device not found")

if dev.is_kernel_driver_active(0):
    dev.detach_kernel_driver(0)

dev.set_configuration()
cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

ep = usb.util.find_descriptor(
    intf,
    custom_match=lambda e:
        usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
)

assert ep is not None

while True:
    try:
        data = dev.read(ep.bEndpointAddress, ep.wMaxPacketSize, timeout=1000)
        raw = data[3]
        scaled = int((raw / 255) * 65535 - 32768)
        device.emit(uinput.ABS_Y, scaled)
    except usb.core.USBError:
        time.sleep(0.005)
