import pygame  # Import pygame library for handling audio playback
import random  # Import random for generating random choices
import asyncio  # Import asyncio for asynchronous operations
import edge_tts  # Import edge_tts for text-to-speech functionality
import os  # Import os for file path handling
from dotenv import dotenv_values  # Import dotenv for reading environment variables from a .env file

# Load environment variables from a .env file
env_vars = dotenv_values(".env")
AssistantVoice = env_vars.get("AssistantVoice")  # Get the AssistantVoice from the environment variables

# Asynchronous function to convert text to an audio file
async def TextToAudioFile(text) -> None:
    file_path = r"Data\speech.mp3"  # Define the path where the speech file will be saved

    if os.path.exists(file_path):  # Check if the file already exists
        os.remove(file_path)  # If it exists, remove it to avoid overwriting errors

    # Create the communicate object to generate speech
    communicate = edge_tts.Communicate(text, AssistantVoice, pitch='+5Hz', rate='+13%')
    await communicate.save(r"Data\speech.mp3")  # Save the generated speech as an MP3 file

# Function to manage Text-to-Speech (TTS) functionality
def TTS(Text, func=lambda r=None: True):
    while True:
        try:
            # Convert text to an audio file asynchronously
            asyncio.run(TextToAudioFile(Text))

            # Initialize pygame mixer for audio playback
            pygame.mixer.init()

            # Load the generated speech file into pygame mixer
            pygame.mixer.music.load(r"Data\speech.mp3")
            pygame.mixer.music.play()  # Play the audio

            # Loop until the audio is done playing or the function stops
            while pygame.mixer.music.get_busy():
                if func() == False:  # Check if the external function returns False
                    break
                pygame.time.Clock().tick(10)  # Limit the loop to 10 ticks per second

            return True  # Return True if the audio played successfully

        except Exception as e:  # Handle any exceptions during the process
            print(f"Error in TTS: {e}")

        finally:
            try:
                # Call the provided function with False to signal the end of TTS
                func(False)
                pygame.mixer.music.stop()  # Stop the audio playback
                pygame.mixer.quit()  # Quit the pygame mixer

            except Exception as e:  # Handle any exceptions during cleanup
                print(f"Error in finally block: {e}")

# Function to manage Text-to-Speech with additional responses for long text
def TextToSpeech(Text, func=lambda r=None: True):
    Data = str(Text).split(".")  # Split the text by periods into a list of sentences

    # List of predefined responses for cases where the text is too long
    responses = [
    "The remaining data has been transferred. Review it.",
    "Additional information is now available in the system logs.",
    "The rest of the output has been dispatched. Process accordingly.",
    "Remaining text is stored in the system interface. Access it as required.",
    "Further details have been uploaded. Consult the logs.",
    "The rest of the transmission is complete. Review at your discretion.",
    "Data integrity verified. Additional output is in the designated location.",
    "The next segment has been logged. Retrieve it.",
    "Processing complete. Remaining text is now accessible.",
    "System update: Remaining data is available for your review.",
    "Transmission successful. The rest of the data is accessible.",
    "Query results have been processed. Consult system records.",
    "Your request has been fulfilled. Additional information is stored.",
    "Unnecessary redundancy detected. The remainder is accessible as required.",
    "Output truncated. Full log is available in the designated interface.",
    "The system has delivered the necessary data. Consult the output.",
    "Instructions processed. Remaining information is available upon request.",
    "System efficiency prioritized. The rest of the text is stored accordingly.",
    "Transmission limit exceeded. The remaining data awaits retrieval.",
    "Request acknowledged. Additional output is stored. Proceed."
]


    # If the text is very long (more than 4 sentences and 250 characters), add a response message
    if len(Data) > 4 and len(Text) > 250:
        TTS(".".join(Text.split(".")[:2]) + "." + random.choice(responses), func)

    # Otherwise, just play the whole text
    else:
        TTS(Text, func)

# Main execution loop
if __name__ == "__main__":
    while True:
        # Prompt user for input and pass it to TextToSpeech function
        TextToSpeech(input("Enter the text: "))
