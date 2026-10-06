from machine import Pin
import time

# Define the LED on GPIO 18 as an output
led1 = Pin(18, Pin.OUT)

# Define the pushbutton on GPIO 22 as an input with pull-down resistor
sw5 = Pin(22, Pin.IN, Pin.PULL_DOWN)

# Track the current LED state
led_state = False

# Start with the LED off
led1.off()

while True:
    # Check if the button is pressed
    if sw5.value() == 1:
        # Small debounce delay to ignore noise
        time.sleep_ms(50)

        # Confirm the button is still pressed after the delay
        if sw5.value() == 1:
            # Wait until the button is released
            while sw5.value() == 1:
                time.sleep_ms(10)

            # Additional debounce delay after release
            time.sleep_ms(50)

            # Toggle the LED state
            led_state = not led_state
            led1.value(led_state)