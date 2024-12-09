import streamlit as st
import numpy as np
import datetime
import pyttsx3
import random
import cv2

try:
    import sounddevice as sd
    from scipy.io.wavfile import write
    audio_enabled = True
except OSError:
    st.warning("Audio recording is disabled because PortAudio is not available.")
    audio_enabled = False

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Simulated GPS coordinates
latitude = 0
longitude = 0

def simulate_gps_data():
    global latitude, longitude
    latitude = np.random.uniform(low=-90, high=90)
    longitude = np.random.uniform(low=-180, high=180)
    return latitude, longitude

def speak(text):
    """Use pyttsx3 to speak a given text."""
    engine.say(text)
    engine.runAndWait()

def send_sos_message(phone_number, message):
    st.write(f"Simulating a call to {phone_number}...")
    st.write("Recording call audio...")

    # Speak SOS message
    speak("This is an SOS call. Please provide assistance.")

    # Record audio during the call (if audio is enabled)
    if audio_enabled:
        fs = 44100  # Sample rate
        seconds = 10  # Record for 10 seconds
        try:
            recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()  # Wait for the recording to finish
            write("call_record.wav", fs, recording)
            st.success("Call recording saved as 'call_record.wav'")
        except Exception as e:
            st.error(f"Failed to record audio: {e}")
    else:
        st.warning("Audio recording is disabled. Skipping this step.")

    # Simulate taking a video
    take_video()

    # Speak Guardian IoT status
    speak("Guardian IoT is now active and monitoring your location.")

    # Send SOS message
    st.success(f"SOS message sent: {message}")
    speak(message)

def take_video():
    """Simulate recording a video."""
    st.write("Recording video...")
    cam = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('emergency_video.avi', fourcc, 20.0, (640, 480))

    for _ in range(50):  # Record a short video
        ret, frame = cam.read()
        if ret:
            out.write(frame)

    out.release()
    cam.release()
    cv2.destroyAllWindows()
    st.success("Video saved as 'emergency_video.avi'")

# Streamlit app setup
def main():
    st.title("Guardian IoT: Women's Safety App")
    st.subheader("Monitoring and Assistance System")

    # Welcome message
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        greeting = "Good Morning!"
    elif 12 <= hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!"
    st.info(greeting + " I am Guardian IoT. How may I assist you?")
    speak(greeting + " I am Guardian IoT. How may I assist you?")

    # Simulate GPS data
    st.subheader("Simulated GPS Coordinates")
    lat, lon = simulate_gps_data()
    st.write(f"Current Location: Latitude {lat}, Longitude {lon}")
    speak(f"Current location coordinates: Latitude {lat}, Longitude {lon}")

    # SOS Button
    if st.button("Trigger SOS"):
        phone_number = "1234567890"  # Replace with actual number
        message = f"SOS! My location is ({lat}, {lon})"
        send_sos_message(phone_number, message)

if __name__ == "__main__":
    main()
