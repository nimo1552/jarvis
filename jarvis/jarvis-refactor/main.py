import threading
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from io_voice import speak, listen_for_voice_command, listen_for_wake_word_thread
from memory import load_memory, save_memory
from skills.system import perform_computer_task

def main():
    memory = load_memory()
    interrupted = threading.Event()
    listening = threading.Event()
    hello_msg = "🤖 Hello! I am Jarvis. How can I assist you today?"
    print(hello_msg)
    speak("Hello! I am Jarvis. Say your custom wake word to activate voice command, or type your question.")
    wake_thread = threading.Thread(target=listen_for_wake_word_thread, args=(listening, interrupted), daemon=True)
    wake_thread.start()
    interrupt_words = ["stop", "cancel", "exit", "quit"]
    try:
        while True:
            while not listening.is_set():
                if interrupted.is_set():
                    break
                threading.Event().wait(0.1)
            if interrupted.is_set():
                print("[Voice] Interruption received. Exiting.")
                break
            while True:
                user_input, interrupted_word = listen_for_voice_command(interrupt_words=interrupt_words)
                listening.clear()
                if interrupted.is_set():
                    print("[Voice] Interruption received during command. Exiting.")
                    return
                if interrupted_word:
                    print("[Voice] Interruption word received. Exiting.")
                    return
                if not user_input:
                    print("[Voice] No command detected. Listening for another command...")
                    continue
                response = perform_computer_task(user_input)
                if response:
                    print(f"Jarvis: {response}")
                    speak(response)
                # Stay in this loop until stop word is spoken
    except KeyboardInterrupt:
        print("[Voice] Keyboard interrupt received. Exiting.")
    finally:
        interrupted.set()
        listening.clear()

if __name__ == "__main__":
    main()
