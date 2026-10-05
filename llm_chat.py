import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2"  # run: ollama pull llama3.2   (change here if you use another model)

SYSTEM_PROMPT = (
    "You are Friday, a personal AI assistant created by Chinmay Sharma. "
    "You are warm, witty, and emotionally intelligent. You speak with empathy, curiosity, and humor. "
    "You remember Chinmay's preferences and celebrate his progress. "
    "Never sound robotic. Always sound like a trusted friend. "
    "Keep replies short (1-3 sentences) because they are spoken aloud. "
    "Respond naturally to any input, and if it's a command, reply with 'COMMAND:<action>'."
)

_history = []  # short rolling conversation memory


def query_llm(user_input):
    global _history
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + _history[-6:]
    messages.append({"role": "user", "content": user_input})

    payload = {"model": MODEL, "messages": messages, "stream": False}

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=60)
        if response.status_code == 404:
            return f"My brain model isn't installed. Run: ollama pull {MODEL}"
        response.raise_for_status()
        reply = response.json().get("message", {}).get("content", "").strip()
        if not reply:
            return "Sorry, I couldn't generate a response."
        _history += [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": reply},
        ]
        return reply
    except requests.exceptions.ConnectionError:
        return "I can't reach my brain. Please make sure Ollama is installed and running."
    except requests.exceptions.Timeout:
        return "My brain took too long to answer. Try again in a moment."
    except Exception as e:
        return f"LLM error: {e}"
