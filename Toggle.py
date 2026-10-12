# toggle.py
# Toggle an LED each time a button is pressed, with software debouncing.
# Debounce method: non-blocking, timestamp based.
# A press is only accepted if at least DEBOUNCE_MS milliseconds have passed
# since the last accepted press. This ignores the button "bounce" without
# using sleep(), so the program is never frozen while waiting.

from machine import Pin
import time

#  Configuration 
LED_PIN = 18         # GPIO pin of the LED (same as the lab example; try 16 if it does not light)
BUTTON_PIN = 22      # GPIO pin of button SW5
DEBOUNCE_MS = 50     # Ignore any button change for 50 ms after a press

#  Hardware setup 
led = Pin(LED_PIN, Pin.OUT)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_DOWN)   # reads 1 when pressed

#  State variables 
led_on = False                    # LED must be off when the program starts
led.off()
last_button_state = button.value()    # button state from the previous loop pass
last_press_time = time.ticks_ms()     # time of the last accepted press

#  Main loop 
while True:
    current_state = button.value()

    # Look for a rising edge: button was released (0) and is now pressed (1)
    if current_state == 1 and last_button_state == 0:
        now = time.ticks_ms()

        # Only accept the press if enough time has passed since the last one
        # (ticks_diff handles the timer wrapping around correctly)
        if time.ticks_diff(now, last_press_time) > DEBOUNCE_MS:
            led_on = not led_on        # flip the LED state
            led.value(led_on)          # update the LED output
            last_press_time = now      # remember when this press happened

    # Save the current state so we can detect the next change
    last_button_state = current_state
