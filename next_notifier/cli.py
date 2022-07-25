from suscribers.blink import Blink
import time
blinker = Blink()
#blinker.notify("green")
time.sleep(2)
blinker.notify("blue")
time.sleep(2)
blinker.notify("green")