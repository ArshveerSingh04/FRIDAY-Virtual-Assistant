from decouple import config

api = config("ELEVEN_API_KEY", default="")
voice = config("ELEVEN_VOICE_ID", default="")

print("API key loaded:", bool(api))
print("Voice ID loaded:", bool(voice))
print("Voice ID:", voice)