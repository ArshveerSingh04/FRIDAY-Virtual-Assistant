import os
import numpy as np
from voiceprint_utils import extract_features

from config_paths import VOICEPRINT_PATH


def is_owner_voice(new_voice_file):
    if not os.path.exists(VOICEPRINT_PATH):
        print(f"❌ Voiceprint file not found at: {VOICEPRINT_PATH}")
        return False

    new_voiceprint = extract_features(new_voice_file)
    saved_voiceprint = np.load(VOICEPRINT_PATH)

    similarity = np.linalg.norm(new_voiceprint - saved_voiceprint)
    print("🔐 Similarity score:", similarity)

    return similarity < 120