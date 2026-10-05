from datetime import datetime
import platform
import psutil


def get_time_greeting():
    hour = datetime.now().hour

    if 5 <= hour < 12:
        return "Good morning."
    elif 12 <= hour < 17:
        return "Good afternoon."
    elif 17 <= hour < 21:
        return "Good evening."
    else:
        return "Hello."


def get_system_config():
    cpu = platform.processor()
    ram_gb = round(psutil.virtual_memory().total / (1024 ** 3), 1)

    return (
        f"Your system configuration is: "
        f"Operating system: {platform.system()} {platform.release()}, "
        f"Processor: {cpu}, "
        f"RAM: {ram_gb} GB."
    )


def hardcoded_response(command):
    command = command.lower().strip()

    # Hello Friday
    if command in (
        "hello friday",
        "hi friday",
        "hey friday",
    ):
        return "Hello Chinmay. Friday is online and ready to assist you."

    # Time-based greetings
    if command == "good morning":
        if 5 <= datetime.now().hour < 12:
            return "Good morning Chinmay. How can I assist you?"
        return "It's not morning anymore, Chinmay. " + get_time_greeting()

    if command == "good afternoon":
        if 12 <= datetime.now().hour < 17:
            return "Good afternoon Chinmay. How can I assist you?"
        return "It's not afternoon anymore, Chinmay. " + get_time_greeting()

    if command == "good evening":
        if 17 <= datetime.now().hour < 21:
            return "Good evening Chinmay. How can I assist you?"
        return "It's not evening anymore, Chinmay. " + get_time_greeting()

    # System configuration
    if (
        "system config" in command
        or "system configuration" in command
        or "pc configuration" in command
        or "computer configuration" in command
        or "my system" in command and "config" in command
    ):
        return get_system_config()

    # Greet someone
    if command.startswith("friday greet "):
        name = command.replace("friday greet ", "", 1).strip()

        if name:
            greeting = get_time_greeting()
            return f"{greeting} {name}. Nice to meet you."

def savage_response(command):
    command = command.lower().strip()

    savage_replies = {
        "are you stupid": "Stupid toh nahi hoon, but tumhare questions meri patience test zaroor kar rahe hain.",
        "are you dumb": "Dumb main nahi, question thoda suspicious hai.",
        "do you love me": "Sir, main AI hoon. Emotional damage ke liye aapko humans ke paas jaana padega.",
        "will you marry me": "Pehle apni life set kar lo, shaadi baad mein discuss karenge.",
        "am i handsome": "Confidence achha hai. Evidence abhi pending hai.",
        "am i ugly": "Main AI hoon, judge nahi. Lekin camera khol ke khud se pooch lo.",
        "do you have a boyfriend": "Nahi. Mere paas server hai, boyfriend nahi.",
        "who is better me or you": "Processing power ki baat hai toh tum already jaante ho answer.",
        "can i ask you personal questions": "bakchodi nahii"
    }

    if command in savage_replies:
        return savage_replies[command]

    # Generic bakchodi triggers
    if "stupid question" in command:
        return "Question dekh ke mujhe bhi do second ke liye system restart karne ka mann hua."

    if "shut up" in command:
        return "Aukaat mein rehne ki advice dene wale khud mujhse baat kar rahe hain."

    return None