import os
import pvporcupine
import pyaudio
import struct
from utils.speech_engine import speak
from friday_core import listen_and_authenticate  # Your assistant loop

ACCESS_KEY = "WDq8oVzIUZkYt4YBS8txfMH9pKMO67E6kCLQJvbdlt+JEaG8sVQV7Q==" # Replace with config("ACCESS_KEY") if using .env

def start_wake_listener():
    # Dynamically resolve keyword file path
    keyword_path = os.path.join(os.path.dirname(__file__), "Hello-Friday.ppn")

    if not os.path.exists(keyword_path):
        raise FileNotFoundError(f"Keyword file not found at: {keyword_path}")

    # Initialize Porcupine wake word engine
    porcupine = pvporcupine.create(
        access_key=ACCESS_KEY,
        keyword_paths=[keyword_path]
    )

    # Set up audio stream
    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("🎙️ Listening for 'Hello Friday'...")

    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            result = porcupine.process(pcm)
            if result >= 0:
                speak("Hello Chinmay, Friday is online.")
                listen_and_authenticate()
    except KeyboardInterrupt:
        print("🛑 Wake listener stopped by user.")
        speak("Wake listener shutting down.")
    except Exception as e:
        print(f"⚠️ Wake listener error: {e}")
        speak("An error occurred in the wake listener.")
    finally:
        audio_stream.close()
        pa.terminate()
        porcupine.delete()