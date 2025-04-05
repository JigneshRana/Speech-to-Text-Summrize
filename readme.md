# AI Voice Conversation System

This project implements an AI-powered voice conversation system that uses speech recognition, AI text generation, and text-to-speech technologies to create a seamless voice interface. The system can understand speech input, process it with AI, and respond audibly using natural-sounding voices.

## Features

- **Speech-to-Text**: Converts spoken language into text using Google Speech Recognition or AssemblyAI
- **AI Text Generation**: Processes the transcribed text using OpenAI GPT-4, Google Gemini, or other LLMs
- **Text-to-Speech**: Converts AI-generated responses into natural-sounding speech using ElevenLabs
- **Continuous Listening Mode**: Accumulates speech until a trigger phrase is detected (in tts3.py)
- **Multiple Implementation Options**: Different scripts for various API combinations

## Project Files

- **tts.py**: Implementation using AssemblyAI for speech recognition and OpenAI for text generation
- **tts2.py**: Implementation using Google Speech API for recognition and Google Gemini for text generation
- **tts3.py**: Enhanced version with continuous listening and speech accumulation until summarization is requested

## Prerequisites

- Python 3.8+
- An active internet connection
- API keys for the services used (OpenAI, ElevenLabs, AssemblyAI, Google Gemini)

## System Dependencies

Before installing Python packages, you need to install PortAudio for audio processing:

```bash
# For Ubuntu/Debian
sudo apt update
sudo apt install portaudio19-dev python3-dev

# For macOS (using Homebrew)
brew install portaudio
```

## Installation

1. Clone or download this repository
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

Create a `.env` file in the project root directory with your API keys:
