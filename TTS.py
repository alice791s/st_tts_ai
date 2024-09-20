# Import necessary libraries
from dotenv import load_dotenv
import os
from deepgram import DeepgramClient, SpeakOptions
# Load environment variables from a .env file
load_dotenv()

# Set the output filename for the audio file
filename = "output.wav"

# Function to convert text to speech using Deepgram's TTS service

def TTS(text):
    try:
        # STEP 1: Create a Deepgram client using the API key from environment variables
        deepgram = DeepgramClient(api_key= os.getenv("API_KEY"))

        # STEP 2: Configure the options (such as model choice, audio configuration, etc.)
        options = SpeakOptions(
            model="aura-asteria-en",
            encoding="linear16",
            container="wav"
        )

        # STEP 3: Call the save method on the speak property
        SPEAK_OPTIONS = {"text": text}
        response = deepgram.speak.v("1").save(filename, SPEAK_OPTIONS, options)
        return filename

    except Exception as e:
        print(f"Exception: {e}")       
        
if __name__ == "__main__":
    text = "Hello, welcome to the Groq Voice Assistant!"
    result = TTS(text)
    if result:
        print(f"Audio saved successfully to {result}")
    else:
        print("Failed to generate audio.")

