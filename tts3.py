import google.generativeai as genai
import speech_recognition as sr
from elevenlabs import play
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import os
import sys
import time

# Redirect stderr to null device to suppress ALSA errors
stderr = sys.stderr
sys.stderr = open(os.devnull, 'w')

# Import PyAudio (which triggers the ALSA warnings)
import speech_recognition as sr

# Restore stderr
sys.stderr = stderr

# Load from .env
load_dotenv()

# Access API keys
gemini_key = os.getenv("GEMINI_API_KEY")
elevenlabs_key = os.getenv("ELEVEN_API_KEY")

# Configure Gemini API
genai.configure(api_key=gemini_key)
model = genai.GenerativeModel('gemini-1.5-pro')

# Initialize the ElevenLabs client with your API key
client = ElevenLabs(api_key=elevenlabs_key)

# Initialize the speech recognizer
recognizer = sr.Recognizer()

# Trigger phrases that will send accumulated text to AI
TRIGGER_PHRASES = ["summarize", "summarize this", "ai summarize", "generate response"]

# Conversation loop
def handle_conversation():
    # Variable to store accumulated speech
    accumulated_speech = ""
    
    print("Starting continuous listening mode...")
    print("Speak freely. Say 'summarize' or 'summarize this' when you want the AI to respond.")
    
    while True:
        # Record audio from the microphone
        with sr.Microphone() as source:
            print("\nListening... (Say 'summarize' to get AI response, or Ctrl+C to exit)")
            
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            
            try:
                # Listen for user input
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
                
                # Use Google's speech recognition
                segment = recognizer.recognize_google(audio)
                print(f"You said: {segment}")
                
                # Add to accumulated speech with a space
                if accumulated_speech:
                    accumulated_speech += " " + segment
                else:
                    accumulated_speech = segment
                
                # Check if any trigger phrase was spoken
                if any(trigger.lower() in segment.lower() for trigger in TRIGGER_PHRASES):
                    print("\nTrigger phrase detected! Sending to AI...")
                    
                    # Generate response using Gemini
                    response = model.generate_content(accumulated_speech)
                    text = response.text
                    
                    # Convert response to audio using ElevenLabs
                    audio = client.text_to_speech.convert(
                        text=text,
                        voice_id="Bella"
                    )
                    
                    print(f"\nAI: {text}")
                    
                    # Play audio
                    play(audio)
                    
                    # Ask if user wants to start a new conversation
                    print("\nDo you want to start a new conversation? Say 'yes' or 'no'")
                    
                    with sr.Microphone() as confirm_source:
                        confirm_audio = recognizer.listen(confirm_source, timeout=5)
                        confirm_response = recognizer.recognize_google(confirm_audio).lower()
                        
                        if "yes" in confirm_response:
                            accumulated_speech = ""
                            print("Starting a new conversation!")
                        else:
                            print("Continuing the current conversation...")
                
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except sr.WaitTimeoutError:
                print("No speech detected, continuing to listen...")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")
                
            # Brief pause to avoid hammering the API
            time.sleep(0.5)

if __name__ == "__main__":
    handle_conversation()