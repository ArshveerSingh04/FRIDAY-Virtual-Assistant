from voiceprint_utils import extract_features
import numpy as np

features = extract_features("my_voice.wav")
np.save("voiceprint.npy", features)
print("Voiceprint saved successfully.")