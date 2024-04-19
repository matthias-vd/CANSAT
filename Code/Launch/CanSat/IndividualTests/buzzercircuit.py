import time
import board
import digitalio

# Define the buzzer pin
buzzer_pin = board.GP26

# Initialize the buzzer pin as a digital output
buzzer = digitalio.DigitalInOut(buzzer_pin)
buzzer.direction = digitalio.Direction.OUTPUT

# Function to play a tone
def play_tone(frequency, duration):
    period = 1.0 / frequency
    delay = period / 2
    cycles = int(duration * frequency)

    for _ in range(cycles):
        buzzer.value = True
        time.sleep(delay)
        buzzer.value = False
        time.sleep(delay)

# Main loop
while True:
    # Play a 1 kHz tone for 0.5 seconds
    play_tone(1000, 0.5)
    time.sleep(0.1)  # Wait for 0.1 seconds between tones
    print("ok")
