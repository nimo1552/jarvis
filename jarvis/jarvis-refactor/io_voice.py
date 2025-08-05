import pyttsx3
import speech_recognition as sr
import pvporcupine
import pyaudio
import numpy as np
import time
import threading


# Use a global lock to prevent concurrent TTS calls
import threading
engine = pyttsx3.init()
_tts_lock = threading.Lock()

def speak(text):
    try:
        with _tts_lock:
            engine.say(text)
            engine.runAndWait()
            time.sleep(0.2)
    except Exception as e:
        print(f"[TTS Error] {e}")

def listen_for_voice_command(interrupt_words=None):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening for your command... (say 'stop' or 'cancel' to interrupt)")
            audio = recognizer.listen(source, phrase_time_limit=8)
        command = recognizer.recognize_google(audio)
        print(f"You said: {command}")
        if interrupt_words and any(word in command.lower() for word in interrupt_words):
            print("[Interruption detected]")
            return (None, True)  # interruption detected
        return (command, False)
    except sr.UnknownValueError:
        print("Sorry, I could not understand your voice.")
        speak("Sorry, I could not understand your voice.")
        return (None, False)
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        speak("Sorry, I could not access the speech service.")
        return (None, False)
    except Exception as e:
        print(f"[Voice Command Error] {e}")
        speak("Sorry, there was a problem with the microphone.")
        return (None, False)

def listen_for_wake_word_thread(listening, interrupted):
    porcupine = pvporcupine.create(
        keyword_paths=["jarvis_en_windows_v3_0_0.ppn"],
        access_key="Nlk0z4mkpOwBAM1KyH+EEfbuJHuk759dWYLdlnWMYmsp6LMYkti98g=="
    )
    pa = pyaudio.PyAudio()
    stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length)
    print("[Wake Word] Real-time listening for your custom 'Jarvis' wake word...")
    try:
        while not interrupted.is_set():
            pcm = stream.read(porcupine.frame_length, exception_on_overflow=False)
            pcm = np.frombuffer(pcm, dtype=np.int16)
            result = porcupine.process(pcm)
            if result >= 0:
                print("Wake word detected! Please speak your command...")
                listening.set()
                speak("Yes?")
                while listening.is_set() and not interrupted.is_set():
                    time.sleep(0.1)
    except Exception as e:
        print(f"[Wake Word Error] {e}")
        speak("Sorry, there was a problem with the wake word engine.")
    finally:
        try:
            stream.stop_stream()
            stream.close()
            pa.terminate()
            porcupine.delete()
        except Exception:
            pass
