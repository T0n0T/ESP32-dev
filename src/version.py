import esp32
from machine import Pin

r = esp32.RMT(0, pin=Pin(18), clock_div=8) # RMT(channel=0, pin=18, source_freq=80000000, clock_div=8, idle_level=0)

# The channel resolution is 100ns (1/(source_freq/clock_div)).
r.write_pulses((1, 20, 2, 40), 0)  # Send 0 for 100ns, 1 for 2000ns, 0 for 200ns, 1 for 4000ns