import sounddevice as sd
import soundfile as sf

def record_voice(filename='my_voice.wav', duration=5, samplerate=48000):
    try:
        print("Recording... Speak now.")
        recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1)
        sd.wait()  # Wait until recording is finished
        sf.write(filename, recording, samplerate)
        print(f"Recording saved as {filename}")
    except Exception as e:
        print("Recording failed:", e)

record_voice()