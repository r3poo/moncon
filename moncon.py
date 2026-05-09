import monitorcontrol
import keyboard
from dotenv import load_dotenv
from os import getenv
import pystray
from PIL import Image
from sys import exit

def on_clicked(icon, item):
    if str(item) == "Exit":
        icon.stop()
        
menu = pystray.Menu(pystray.MenuItem("Exit", on_clicked))
iconimage = Image.radial_gradient("L")
icon = pystray.Icon("app", iconimage, "mon controller", menu)



if not load_dotenv():
    exit()
mons = monitorcontrol.monitorcontrol.get_monitors()

MON_ON=getenv("MON_ON")
MON_OFF=getenv("MON_OFF")
BRIGHTNESS_UP=getenv("BRIGHTNESS_UP")
BRIGHTNESS_DOWN=getenv("BRIGHTNESS_DOWN")

        
def brightnessUp(delta: int=5):
    for mon in mons:
        with mon as m:
            val = min(100, m.get_luminance()+delta)
            m.set_luminance(val)

def brightnessDown(delta: int=5):
    for mon in mons:
        with mon as m:
            val = max(0, m.get_luminance()-delta)
            m.set_luminance(val)

def monOff():
    for mon in mons:
        with mon as m:
            m.set_power_mode(monitorcontrol.PowerMode.off_soft)

def monOn():
    for mon in mons:
        with mon as m:
            m.set_power_mode(monitorcontrol.PowerMode.on)


keyboard.add_hotkey(BRIGHTNESS_UP, brightnessUp, suppress=True, trigger_on_release=True)
keyboard.add_hotkey(BRIGHTNESS_DOWN, brightnessDown, suppress=True, trigger_on_release=True)
keyboard.add_hotkey(MON_OFF, monOff, suppress=True, trigger_on_release=True)
keyboard.add_hotkey(MON_ON, monOn, suppress=True, trigger_on_release=True)

icon.run()