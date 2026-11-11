from machine import Pin, PWM
from time import sleep
from servo_translator import translate


def parse_line(line):
    # Remove extra spaces and skip empty lines.
    line = line.strip()

    if line == "":
        return None, {}

    parts = line.split()
    command = parts[0]
    parameters = {}

    # Example: S62.858 becomes {"S": 62.858}.
    for part in parts[1:]:
        letter = part[0]
        value = float(part[1:])
        parameters[letter] = value

    return command, parameters


def disable_servos(shoulder, elbow, wrist):
    # A zero duty cycle stops the control pulses.
    shoulder.duty_u16(0)
    elbow.duty_u16(0)
    wrist.duty_u16(0)


def run_command(command, parameters, shoulder, elbow, wrist):
    if command == "G1":
        # Only move a servo if its parameter is present.
        if "S" in parameters:
            shoulder.duty_u16(translate(parameters["S"]))

        if "E" in parameters:
            elbow.duty_u16(translate(parameters["E"]))

        # Give the servos time to move.
        sleep(0.2)

    elif command == "M3":
        # Lower the pen.
        wrist.duty_u16(translate(30))
        sleep(0.3)

    elif command == "M5":
        # Raise the pen.
        wrist.duty_u16(translate(0))
        sleep(0.3)

    elif command == "M18":
        disable_servos(shoulder, elbow, wrist)

    else:
        raise ValueError("Unknown command: " + command)


def main():
    shoulder = PWM(Pin(0))
    elbow = PWM(Pin(1))
    wrist = PWM(Pin(2))

    shoulder.freq(50)
    elbow.freq(50)
    wrist.freq(50)

    try:
        # Change this filename to draw a different shape.
        with open("line.gcode", "r") as file:
            for line in file:
                command, parameters = parse_line(line)

                if command is not None:
                    run_command(
                        command, parameters,
                        shoulder, elbow, wrist
                    )

    finally:
        # Stop the signals when finished or if an error occurs.
        disable_servos(shoulder, elbow, wrist)
        shoulder.deinit()
        elbow.deinit()
        wrist.deinit()


main()