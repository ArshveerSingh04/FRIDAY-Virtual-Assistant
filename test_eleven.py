from decouple import config
from elevenlabs import ElevenLabs

api_key = config("ELEVEN_API_KEY")
voice_id = config("ELEVEN_VOICE_ID")

print("API loaded:", bool(api_key))
print("Voice loaded:", bool(voice_id))
print("Voice ID:", voice_id)

try:
    client = ElevenLabs(api_key=api_key)

    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        text="Hello Chinmay. FRIDAY is back online.",
    )

    with open("friday_test.mp3", "wb") as f:
        for chunk in audio:
            f.write(chunk)

    print("SUCCESS! Audio generated: friday_test.mp3")

except Exception as e:
    print("\n========== ELEVENLABS ERROR ==========")
    print(type(e).__name__)
    print(str(e))
    print("======================================")