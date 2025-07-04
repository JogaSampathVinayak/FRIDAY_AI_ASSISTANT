import whisper
import sounddevice as sd
import numpy as np
import tempfile
import scipy.io.wavfile

model = whisper.load_model("base")

def take_command(language_code="en"):
    try:
        print("🎧 Listening...")
        duration = 5
        fs = 44100
        audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            scipy.io.wavfile.write(f.name, fs, audio)
            result = model.transcribe(f.name, language=language_code)
            return result['text']
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None
