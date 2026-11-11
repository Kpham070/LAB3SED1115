def translate(angle: float) -> int:
    """Convert an angle to a servo PWM value."""

    # Keep the angle between 0 and 180 degrees.
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180

    # Calculate the pulse width.
    pulse_width = 500 + 2000 * angle / 180

    # Convert it to a duty_u16 value.
    duty = int(pulse_width / 20000 * 65535)

    return duty