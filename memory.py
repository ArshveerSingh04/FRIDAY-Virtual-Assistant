from config_paths import MEMORY_PATH
import json
import os
def load_memory():
    if not os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH, "w") as f:
            json.dump({}, f)

    with open(MEMORY_PATH, "r") as f:
        return json.load(f)

def update_memory(key, value):
    memory = load_memory()
    memory[key] = value
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)