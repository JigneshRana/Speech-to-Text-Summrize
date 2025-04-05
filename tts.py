import assemblyai as aai
import openai
from elevenlabs import play  # Import play function
from elevenlabs.client import ElevenLabs  # Import the client
from queue import Queue
from dotenv import load_dotenv
import os

# Load from .env
load_dotenv()

# Access API keys
openai_key = os.getenv("OPENAI_API_KEY")
assemblyai_key = os.getenv("ASSEMBLYAI_API_KEY")
elevenlabs_key = os.getenv("ELEVEN_API_KEY")

# Set API keys
aai.settings.api_key = assemblyai_key
openai.api_key = openai_key

# Initialize the ElevenLabs client with your API key
client = ElevenLabs(api_key=elevenlabs_key)

transcript_queue = Queue()

def on_data(transcript: aai.RealtimeTranscript):
    if not transcript.text:
        return
    if isinstance(transcript, aai.RealtimeFinalTranscript):
        transcript_queue.put(transcript.text + '')
        print("User:", transcript.text, end="\r\n")
    else:
        print(transcript.text, end="\r")

def on_error(error: aai.RealtimeError):
    print("An error occurred:", error)

# Conversation loop
def handle_conversation():
    while True:
        transcriber = aai.RealtimeTranscriber(
            on_data=on_data,
            on_error=on_error,
            sample_rate=44_100,
        )

        # Start the connection
        transcriber.connect()

        # Open the microphone stream
        microphone_stream = aai.extras.MicrophoneStream()

        # Stream audio from the microphone
        transcriber.stream(microphone_stream)

        # Close current transcription session with Ctrl + C
        transcriber.close()

        # Retrieve transcribed text
        transcript_result = transcript_queue.get()

        # Send the transcript to OpenAI for response generation
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {"role": "system", "content": 'You are a highly skilled AI, answer the questions given within a maximum of 1000 characters.'},
                {"role": "user", "content": transcript_result}
            ]
        )

        text = response['choices'][0]['message']['content']

        # Convert response to audio using the new API
        audio = client.text_to_speech.convert(
            text=text,
            voice_id="Bella"
        )

        print("\nAI:", text, end="\r\n")

        # Play audio
        play(audio)

handle_conversation()
