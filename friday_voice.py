
from elevenlabs import ElevenLabs 

# Replace with your API key
API_KEY = "sk_cd45192ab089e0448a725d7f3686f0d09bbbc6c93b752661"
VOICE_ID = "JuoEXc0X8kgfliy2JcOd"

client = ElevenLabs(api_key=API_KEY)

def speak(text):
    audio_stream = client.text_to_speech.convert(
        voice_id=VOICE_ID,
        model_id="eleven_multilingual_v2",
        text=text
    )

    with open("friday.wav", "wb") as f:
        for chunk in audio_stream:
            f.write(chunk)

    # Play using OS default player
    import os
    os.system("start friday.wav")   # Windows
    # os.system("afplay friday.wav") # Mac
    # os.system("xdg-open friday.wav") # Linux

speak("Hello Sir, FRIDAY is now alive in her new voice.")