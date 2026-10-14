
from machine import UART, Pin
import sys
import select
import time

# setting up
uart = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))
uart.init(bits=8, parity=None, stop=1)

#ccheck for keyboard input
keyboard = select.poll()
keyboard.register(sys.stdin, select.POLLIN)

typed = ""
received = b""
last_sent = time.ticks_ms()

print("Pico chat is ready. Type a message and press Enter.")

while True:

    # send the message typed by the user 
    if keyboard.poll(0):
        char = sys.stdin.read(1)

        if char == "\n" or char == "\r":
            if typed.strip():
                uart.write(typed + "\n")
                print("You: " + typed)
                last_sent = time.ticks_ms()
            typed = ""

        elif char == "\b" or char == "\x7f":
            typed = typed[:-1]

        elif len(typed) < 100:
            typed += char

    # receive message frin the other pico
    if uart.any():
        data = uart.read()

        if data:
            received += data

            while b"\n" in received:
                line, received = received.split(b"\n", 1)
                print("Other Pico: " + line.decode().strip())

            if len(received) > 256:
                received = b""

    if time.ticks_diff(time.ticks_ms(), last_sent) >= 10000:
        clock = time.localtime()

        local_time = "{:02d}:{:02d}:{:02d}".format(
            clock[3], clock[4], clock[5]
        )

        uart.write("Keep alive: " + local_time + "\n")
        last_sent = time.ticks_ms()

    time.sleep_ms(10)
