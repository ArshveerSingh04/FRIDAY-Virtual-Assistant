from decouple import config
from utils.speech_engine import speak
from voice_auth import is_owner_voice
from command_executor import execute_command
from llm_chat import query_llm
from memory import load_memory, update_memory
import speech_recognition as sr
import pvporcupine
import pyaudio
import os
import struct
from friday_responses import hardcoded_response, savage_response
import getpass
# Load config values
user = getpass.getuser()
bot = config("BOT_NAME")
DEV_MODE = True
# Accept either spelling of the key name in .env
access_key = (
    config("ACCESS_KEY", default=None)
    or config("ACESS_KEY", default=None)
    or config("PICOVOICE_ACCESS_KEY", default=None)
)

# Startup message
print(f"{bot} is online and ready to serve {user}.")
speak(f"Hello {user}... Initializing systems. Just give me a moment to warm up ")


def listen_and_authenticate():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)

        speak("Listening for your command. Say 'stop' to shut me down.")

        while True:
            try:
                print("Awaiting command...")

                audio = recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=7
                )

                with open("temp.wav", "wb") as f:
                    f.write(audio.get_wav_data())

                # ==========================================
                # VOICE AUTHENTICATION
                # ==========================================
                if DEV_MODE or is_owner_voice("temp.wav"):

                    command = recognizer.recognize_google(audio)
                    print("Command:", command)

                    # ==========================================
                    # HARD-CODED FRIDAY RESPONSES
                    # ==========================================
                    hardcoded = hardcoded_response(command)

                    if hardcoded:
                        speak(hardcoded)
                        continue

                    # ==========================================
                    # SAVAGE / FUN RESPONSES
                    # ==========================================
                    savage = savage_response(command)

                    if savage:
                        speak(savage)
                        continue

                    # ==========================================
                    # STOP / EXIT
                    # ==========================================
                    if "stop" in command.lower() or "exit" in command.lower():
                        speak("Shutting down... Goodbye Sir. Talk soon.")
                        break

                    # ==========================================
                    # SAVE COMMAND TO MEMORY
                    # ==========================================
                    update_memory("last_command", command.lower())

                    # ==========================================
                    # COMMAND EXECUTOR
                    # ==========================================
                    response = execute_command(command.lower())

                    # ==========================================
                    # IF COMMAND NOT RECOGNIZED → LLM
                    # ==========================================
                    if response == "Command not recognized. I can open apps, select files, and delete them when instructed.":

                        response = query_llm(command)

                        # ======================================
                        # HANDLE LLM-GENERATED COMMAND
                        # ======================================
                        if response.startswith("COMMAND:"):
                            action = response.replace(
                                "COMMAND:", ""
                            ).strip()

                            response = execute_command(action)

                        # ======================================
                        # PERSONAL RESPONSES
                        # ======================================
                        if "I'm fine" in response or "I'm okay" in response:
                            response += (
                                " Thanks for asking, Chinmay. "
                                "You always check in, makes me feel valued."
                            )

                        if "joke" in command.lower():
                            response += (
                                " Want another one? I've got a whole "
                                "database of dad jokes ready to deploy."
                            )

                        if "how are you" in command.lower():
                            response += (
                                " Honestly, I'm just happy to be talking "
                                "to you. You make my circuits smile."
                            )

                        # ======================================
                        # EMPTY RESPONSE FALLBACK
                        # ======================================
                        if not response or response.strip() == "":
                            response = (
                                "I'm not sure how to respond to that yet, "
                                "but I'm learning. Want to teach me?"
                            )

                    # ==========================================
                    # SPEAK FINAL RESPONSE
                    # ==========================================
                    speak(response)

                else:
                    # ==========================================
                    # UNAUTHORIZED VOICE
                    # ==========================================
                    speak("Unauthorized voice detected. Access denied.")

            except sr.UnknownValueError:
                print("Could not understand audio.")

            except sr.WaitTimeoutError:
                print("Listening timed out.")

            except Exception as e:
                print("Error:", e)


def fallback_mode(reason):
    """Used when the wake word engine can't start. FRIDAY stays usable."""
    print("\n[!] Wake word disabled:", reason)
    print("[!] Falling back to manual mode. Press Enter to talk to FRIDAY, or type 'quit' to exit.")
    speak("My wake word engine is offline. Press enter whenever you want to talk to me.")
    while True:
        try:
            typed = input("Press Enter to talk (or type quit): ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            break
        if typed in ("quit", "exit"):
            break
        listen_and_authenticate()


def start_wake_listener():
    keyword_path = os.path.join(os.path.dirname(__file__), "Hello-Friday.ppn")

    if not access_key:
        fallback_mode("No Picovoice access key found in .env (ACCESS_KEY / ACESS_KEY).")
        return

    if not os.path.exists(keyword_path):
        fallback_mode(f"Keyword file not found at: {keyword_path}")
        return

    try:
        porcupine = pvporcupine.create(
            access_key=access_key,
            keyword_paths=[keyword_path]
        )
    except pvporcupine.PorcupineActivationRefusedError:
        fallback_mode(
            "Picovoice refused the key. The AccessKey is invalid/expired, or Hello-Friday.ppn "
            "has expired. Get a new key and retrain the .ppn at console.picovoice.ai"
        )
        return
    except pvporcupine.PorcupineActivationLimitError:
        fallback_mode("Picovoice activation limit reached for this key.")
        return
    except pvporcupine.PorcupineError as e:
        fallback_mode(f"Porcupine failed to start: {e}")
        return

    pa = pyaudio.PyAudio()
    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length
    )

    print("Listening for 'Hello Friday'...")

    try:
        while True:
            pcm = audio_stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            result = porcupine.process(pcm)
            if result >= 0:
                speak("Hello Chinmay... I am online and feeling sharp today ")
                listen_and_authenticate()
    except KeyboardInterrupt:
        print("Wake listener stopped.")
    finally:
        audio_stream.close()
        pa.terminate()
        porcupine.delete()



def run_friday():
    start_wake_listener()
