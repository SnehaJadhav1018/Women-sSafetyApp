import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import pyttsx3
import datetime
import random
import cv2

# Simulated GPS coordinates (numerical)
latitude = 0
longitude = 0

# Initialize text-to-speech engine
engine = pyttsx3.init()

def simulate_gps_data():
    global latitude, longitude
    latitude = np.random.uniform(low=-90, high=90)
    longitude = np.random.uniform(low=-180, high=180)
    return latitude, longitude

def simulate_send_message(message):
    print(f"Simulated message sent: {message}")
    speak(message)

def send_sos_message(phone_number, message):
    print(f"Simulating a call to {phone_number}...")

    # Record audio during the call
    fs = 44100  # Sample rate
    seconds = 30  # 30 seconds for call recording

    print("Recording call audio...")
    speak("This is an SOS call. Please provide assistance.")
    recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()  # Wait for recording to finish

    print("Call recording finished. Saving to call_record.wav...")
    write("call_record.wav", fs, recording)
    print("Call recording saved successfully.")

    # Simulate taking a video
    take_video()

    # Speak about Guardian IoT status
    speak("Guardian IoT is now active and monitoring your location.")

    # Send SOS message
    print(f"Sending SOS message: {message}")
    speak(message)

def check_for_sos_button():
    user_input = input("Press 's' to trigger SOS or any other key to continue: ")
    return user_input.lower() == 's'

def setup():
    print("Guardian IoT virtual simulation started...")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def guardian_iot_welcome():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"

    speak(greeting)
    speak("I am Guardian IoT. How may I assist you?")

def take_video():
    print("Recording video...")
    cam = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('emergency_video.avi', fourcc, 20.0, (640, 480))

    for _ in range(100):
        ret, frame = cam.read()
        if ret:
            out.write(frame)

    out.release()
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    setup()  # Call setup() for GPS simulation
    guardian_iot_welcome()

    while True:
        lat, lon = simulate_gps_data()
        print("Simulated GPS coordinates:", lat, lon)
        speak(f"Current location coordinates: Latitude {lat}, Longitude {lon}")

        if lat < 0:
            simulate_send_message("You are safe.")

        # Check for SOS button press
        if check_for_sos_button():
            phone_number = "8830865818"  # Replace with actual number
            message = f"SOS! My location is ({lat}, {lon})"
            send_sos_message(phone_number, message)
            break  # Exit the loop after sending SOS message
