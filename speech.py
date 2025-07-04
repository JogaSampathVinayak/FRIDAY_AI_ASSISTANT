import pyttsx3

engine = pyttsx3.init()
voices = engine.getProperty('voices')

def set_voice(language_code="english"):
    match = next((v for v in voices if language_code in v.name.lower()), None)
    if match:
        engine.setProperty('voice', match.id)
        print(f"✅ Voice set to {match.name}")
    else:
        print("⚠️ Default voice used.")

def speak(text):
    engine.say(text)
    engine.runAndWait()
