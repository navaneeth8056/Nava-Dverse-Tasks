import pyttsx3
import keyboard
import time

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech

# Key descriptions
keys_info = [
    ("forward", "Press the 'right arrow' key to move forward."),
    ("backward", "Press the 'left arrow' key to move backward."),
    ("pause", "Press the 'space' key to pause."),
    ("play", "Press the 'enter' key to play."),
    ("increase volume", "Press the '+' key to increase volume."),
    ("decrease volume", "Press the '-' key to decrease volume."),
    ("skip paragraph", "Press the 'enter' key to skip the paragraph.")
]

# Mapping key names to actual keyboard keys
key_map = {
    "forward": "right",
    "backward": "left",
    "pause": "space",
    "play": "enter",
    "increase volume": "+",
    "decrease volume": "-",
    "skip paragraph": "enter"
}

def speak(text):
    """Speak the given text."""
    engine.say(text)
    engine.runAndWait()

def wait_for_correct_key(correct_key):
    """Wait for the user to press the specified key, handling incorrect inputs."""
    speak(f"Waiting for you to press the {correct_key} key.")
    print(f"Waiting for you to press: {correct_key}")
    while True:
        # Check if the correct key is pressed
        if keyboard.is_pressed(correct_key):
            print(f"{correct_key} pressed!")
            speak(f"{correct_key} pressed!")
            time.sleep(0.5)  # Prevent multiple detections
            break
        # Detect other key presses
        event = keyboard.read_event()
        if event.event_type == "down" and event.name != correct_key:
            print(f"Wrong key: {event.name}. Please press: {correct_key}")
            speak("You pressed the wrong key. Please press the correct key.")

def tutorial():
    """Run the tutorial."""
    # Welcome message
    speak("Welcome to the CuriO tutorial. Press any key to acknowledge learning.")
    print("Welcome to the CuriO tutorial. Press any key to acknowledge learning.")
    
    # Wait for any key to acknowledge learning
    while True:
        event = keyboard.read_event()
        if event.event_type == "down":  # Trigger on key press
            print(f"Acknowledged with key: {event.name}")
            speak("Acknowledged. Let's begin the tutorial.")
            break
    
    # Introduce each key
    for key_name, key_description in keys_info:
        speak(key_description)
        print(key_description)
        wait_for_correct_key(key_map[key_name])

    # End of tutorial
    speak("Congratulations! You have completed the tutorial.")
    print("Congratulations! You have completed the tutorial.")

# Run the tutorial
if __name__ == "__main__":
    tutorial()


"""
 import pyttsx3
import serial
import time

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech

# Serial port configuration for Arduino
arduino_port = "COM3"  # Replace with your Arduino's COM port
baud_rate = 9600
arduino = serial.Serial(arduino_port, baud_rate, timeout=1)

# Button mapping from Arduino
button_map = {
    "1": "forward",  # Button 1: Forward
    "2": "backward",  # Button 2: Backward
    "3": "pause",  # Button 3: Pause
    "4": "play",  # Button 4: Play
    "5": "increase volume",  # Button 5: Increase volume
    "6": "decrease volume"  # Button 6: Decrease volume
}

def speak(text):
    #Speak the given text.
    engine.say(text)
    engine.runAndWait()

def wait_for_arduino_button(expected_button):
    #Wait for the user to press the correct Arduino button.
    speak(f"Waiting for button {expected_button}.")
    print(f"Waiting for button {expected_button}.")
    while True:
        if arduino.in_waiting > 0:
            button_pressed = arduino.readline().decode('utf-8').strip()
            if button_pressed == expected_button:
                print(f"Button {button_pressed} pressed!")
                speak(f"Button {button_pressed} pressed!")
                time.sleep(0.5)  # Prevent multiple detections
                break
            else:
                speak("You pressed the wrong button. Please press the correct button.")
                print(f"Wrong button: {button_pressed}. Please press: {expected_button}")

# Example usage
if __name__ == "__main__":
    for button, action in button_map.items():
        print(f"Action: {action}")
        speak(f"Press the button for {action}.")
        wait_for_arduino_button(button)

 """