import pyttsx3
import keyboard
import time

# Initialize TTS engine
engine = pyttsx3.init()

# Dictionary to map keys to their respective audio messages
key_audio_map = {
    'f1': "Turning on or off",
    'f2': "Volume up",
    'f3': "Volume down",
    'f4': "Fast forwarding",
    'f5': "Pausing",
    'f6': "Moving to the next paragraph"
}

# Function to speak the audio message
def speak_message(message):
    engine.say(message)
    engine.runAndWait()

print("Press ESC to stop")

try:
    while True:
        # Check if the ESC key is pressed to exit the loop
        if keyboard.is_pressed('esc'):
            print("Exiting program.")
            break
        
        # Loop through each key and check if it's pressed
        for key, message in key_audio_map.items():
            if keyboard.is_pressed(key):
                speak_message(message)
                
                # Wait a short moment to prevent the TTS engine from repeating too quickly
                time.sleep(0.5)
        
except KeyboardInterrupt:
    print("Program interrupted by user.")
finally:
    engine.stop()


######################################################################################################################
#program for an external key
"""
import RPi.GPIO as GPIO
import pyttsx3
import time

# Initialize TTS engine
engine = pyttsx3.init()

# Dictionary to map GPIO pins to their respective audio messages
key_audio_map = {
    17: "Turning on or off",          # GPIO pin 17 for On/Off button
    27: "Volume up",                  # GPIO pin 27 for Volume Up
    22: "Volume down",                # GPIO pin 22 for Volume Down
    23: "Fast forwarding",            # GPIO pin 23 for Fast Forward
    24: "Pausing",                    # GPIO pin 24 for Pause
    25: "Moving to the next paragraph"  # GPIO pin 25 for Next Paragraph
}

# Function to speak the audio message
def speak_message(message):
    engine.say(message)
    engine.runAndWait()

# Function to handle button press and trigger appropriate audio output
def button_callback(channel):
    if channel in key_audio_map:
        message = key_audio_map[channel]
        speak_message(message)

# Setup GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM GPIO numbering

# Setup each GPIO pin as input with pull-down resistor
for pin in key_audio_map.keys():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(pin, GPIO.RISING, callback=button_callback, bouncetime=300)

try:
    print("Waiting for button presses. Press CTRL+C to exit.")
    while True:
        # Loop indefinitely
        time.sleep(0.1)  # Small delay to reduce CPU usage
except KeyboardInterrupt:
    print("Exiting program.")

finally:
    GPIO.cleanup()  # Clean up GPIO pins on exit
"""