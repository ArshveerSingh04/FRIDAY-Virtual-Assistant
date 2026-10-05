# FRIDAY - Virtual Assistant

FRIDAY is a voice-based virtual assistant designed to provide users with a natural voice interaction interface. The project uses speech recognition, wake-word detection, and voice authentication to receive and process user commands.

## Voice Module

The Voice Module is responsible for handling voice-based interaction between the user and FRIDAY.

### Working Flow

Microphone Input  
→ Wake Word Detection  
→ Speech Recognition  
→ Voice Authentication  
→ Command Processing  
→ FRIDAY Response

## Technologies Used

- Python
- Picovoice Porcupine - Wake-word detection
- SpeechRecognition - Speech-to-text conversion
- PyAudio - Microphone and audio input
- Librosa - Audio processing and MFCC feature extraction
- NumPy - Numerical operations and feature comparison

## Main Components

### 1. Wake Word Detection

Picovoice Porcupine is used to detect the predefined wake phrase **"Hello Friday"**. Once the wake word is detected, FRIDAY starts listening for the user's command.

### 2. Speech Recognition

The SpeechRecognition library is used to capture the user's spoken command and convert it into text.

### 3. Voice Authentication

The system extracts voice features from the recorded audio using **MFCC (Mel-Frequency Cepstral Coefficients)**.

These features are compared with the stored voice representation using a threshold-based approach to determine whether the speaker is authenticated.

### 4. Audio Processing

Librosa is used for loading and processing audio signals and extracting MFCC features. NumPy is used for numerical calculations and comparison of extracted features.

## Project Files

- `wake_listener.py` - Handles wake-word detection and voice input.
- `voice_auth.py` - Handles voice authentication.
- `voiceprint_utils.py` - Contains utility functions for voice feature processing.

## Security Note

Voiceprint data and API credentials are not included in this repository. Sensitive files and credentials should be stored locally or through environment variables.

## Future Improvements

- Improve voice authentication accuracy.
- Add better noise reduction.
- Support multiple users.
- Improve command recognition in noisy environments.
- Add additional voice-based commands and features.

## Project Status

This project is currently a prototype developed for academic purposes.
