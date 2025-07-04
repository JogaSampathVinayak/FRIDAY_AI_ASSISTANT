import queue
import sounddevice as sd
from vosk import Model, KaldiRecognizer
import json
import threading

q = queue.Queue()
model = Model("models/vosk_model")
rec = KaldiRecognizer(model, 16000)

def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))

def wake_listener(callback_on_wake):
    print("🎧 Always listening for 'Hey Friday'...")
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16', channels=1, callback=audio_callback):
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "").lower()
                if "hey friday" in text:
                    print("🛑 Wake word detected!")
                    callback_on_wake()
