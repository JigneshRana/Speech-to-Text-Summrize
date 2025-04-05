import google.generativeai as genai
import speech_recognition as sr
from elevenlabs import play
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv
import os

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

# Conversation loop
def handle_conversation():
    while True:
        # Record audio from the microphone
        with sr.Microphone() as source:
            print("Listening... (Press Ctrl+C to exit)")
            
            # Adjust for ambient noise
            recognizer.adjust_for_ambient_noise(source)
            
            try:
                # Listen for user input
                audio = recognizer.listen(source, timeout=5)
                
                # Use Google's speech recognition
                transcript_result = recognizer.recognize_google(audio)
                print("User:", transcript_result)
                
                # Generate response using Gemini
                response = model.generate_content(transcript_result)
                text = response.text
                
                # Convert response to audio using ElevenLabs
                audio = client.text_to_speech.convert(
                    text=text,
                    voice_id="Bella"
                )
                
                print("\nAI:", text)
                
                # Play audio
                play(audio)
                
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

if __name__ == "__main__":
    handle_conversation()