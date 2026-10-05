import os
import asyncio
import tempfile

import pygame
import pyttsx3
from decouple import config

# ---- Settings (put these in .env, never hardcode keys) ----
ELEVEN_API_KEY = config("ELEVEN_API_KEY", default="")
ELEVEN_VOICE_ID = config("ELEVEN_VOICE_ID", default="")
EDGE_VOICE = config("EDGE_VOICE", default="en-IE-EmilyNeural")  # free, no key needed

_eleven_client = None
_eleven_disabled = not (ELEVEN_API_KEY and ELEVEN_VOICE_ID)
_edge_disabled = False
_fallback_engine = None
_mixer_ready = False

if not _eleven_disabled:
    try:
        from elevenlabs import ElevenLabs
        _eleven_client = ElevenLabs(api_key=ELEVEN_API_KEY)
    except Exception as e:
        print(f"ElevenLabs unavailable: {e}")
        _eleven_disabled = True


def _play_mp3_bytes(audio_bytes: bytes):
    """Play MP3 data with pygame (no ffmpeg/pydub needed)."""
    global _mixer_ready
    if not _mixer_ready:
        pygame.mixer.init()
        _mixer_ready = True

    fd, path = tempfile.mkstemp(suffix=".mp3")
    try:
        with os.fdopen(fd, "wb") as f:
            f.write(audio_bytes)
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


def _speak_elevenlabs(text: str):
    stream = _eleven_client.text_to_speech.convert(
        voice_id=ELEVEN_VOICE_ID,
        model_id="eleven_multilingual_v2",
        text=text,
    )
    _play_mp3_bytes(b"".join(stream))


def _speak_edge(text: str):
    import edge_tts

    async def _gen():
        communicate = edge_tts.Communicate(text, EDGE_VOICE)
        data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                data += chunk["data"]
        return data

    _play_mp3_bytes(asyncio.run(_gen()))


def _speak_pyttsx3(text: str):
    global _fallback_engine
    if _fallback_engine is None:
        _fallback_engine = pyttsx3.init()
        _fallback_engine.setProperty("rate", 180)
        _fallback_engine.setProperty("volume", 0.9)
    _fallback_engine.say(text)
    _fallback_engine.runAndWait()


def speak(text: str):
    global _eleven_disabled, _edge_disabled

    if not text or not text.strip():
        return

    # 1) ElevenLabs (only if configured and still working)
    if not _eleven_disabled:
        try:
            _speak_elevenlabs(text)
            return
        except Exception as e:
            msg = str(e)
            # Auth / plan problems won't fix themselves, so stop retrying this session
            if any(code in msg for code in ("401", "402", "403", "payment_required", "quota")):
                print("ElevenLabs disabled for this session (plan/key issue). Using edge-tts.")
                _eleven_disabled = True
            else:
                print(f"ElevenLabs error: {e}")

    # 2) edge-tts (free, natural)
    if not _edge_disabled:
        try:
            _speak_edge(text)
            return
        except ImportError:
            print("edge-tts not installed. Run: pip install edge-tts")
            _edge_disabled = True
        except Exception as e:
            print(f"edge-tts error: {e}")

    # 3) Offline robotic fallback
    _speak_pyttsx3(text)