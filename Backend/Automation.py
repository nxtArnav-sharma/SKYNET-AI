# Import required libraries
from AppOpener import close, open as appopen  # Import functions to open and close apps.
from webbrowser import open as webopen  # Import web browser functionality.
from pywhatkit import search, playonyt  # Import functions for Google search and YouTube playback.
from dotenv import dotenv_values  # Import dotenv to manage environment variables.
from bs4 import BeautifulSoup  # Import BeautifulSoup for parsing HTML content.
from rich import print  # Import rich for styled console output.
from groq import Groq  # Import Groq for AI chat functionalities.
import webbrowser  # Import webbrowser for opening URLs.
import subprocess  # Import subprocess for interacting with the system.
import requests  # Import requests for making HTTP requests.
import keyboard  # Import keyboard for keyboard-related actions.
import asyncio  # Import asyncio for asynchronous programming.
import os  # Import os for operating system functionalities.

# Load environment variables from the .env file.
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")  # Retrieve the Groq API key.

# Define CSS classes for parsing specific elements in HTML content.
classes = ["ZGLOWf", "hgKELc", "LIKOO sY/ric", "ZoLCW", "gsrt vk_bk FzWNSb VwPhnf", "pclqec", "tw-Data-text tw-text-small tw-ta",  
    "IZGrdc", "O5uR6d LIKOO", "VlZY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikbABb gsrt", "sXLa0e",  
    "LMKKe", "QyF+g", "qv3Wpe", "kno-rdesc", "SPZZ6b"]  

# Define a user-agent for making web requests.  
useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.126 Safari/537.36"  

# Initialize the Groq client with the API key.  
client = Groq(api_key=GroqAPIKey)  

# Predefined professional responses for user interactions.  
professional_responses = [  
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.",  
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",  
]  

# List to store chatbot messages.  
messages = []  

# System message to provide context to the chatbot.
SystemCastor = {"role": "system", "content": f"Hello, I am {os.environ.get('username')}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}

# Bootstrap function for Google search.
def GoogleSearch(Topic):
    search(Topic)  # Use pywhatkit's search function to perform a Google search.
    return True  # Indicate success.

# Function to generate content using AI and save it to a file.
def Content(Topic):
    # Function to open file in a text editor.
    def OpenMessage(file):
        default_text_editor = 'notepad.exe'  # Default text editor.
        subprocess.Popen([default_text_editor, file])  # Open the file in the text editor.

    # Function to generate content using the AI chatbot.
    def ContentWriterId(prompt):
        messages.append({"role": "user", "content": prompt})  # Add the user's prompt to messages.

        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768",  # Use a valid Groq model
            messages=[SystemCastor] + messages,  # Include system instructions and chat history
            max_tokens=1000,  # Limit the response length
            temperature=0.7,  # Adjust response creativity
            top_p=1,  # Use nucleus sampling for response diversity
            stream=True,  # Enable streaming responses
        )

        Answer = ""  # Initialize an empty string for the response.

        # Process streamed response chunks.
        for chunk in completion:
            if chunk.choices[0].delta.content:  # Check for content in the current chunk.
                Answer += chunk.choices[0].delta.content  # Append the content to the answer.

        Answer = Answer.replace("\\n", "\n")  # Remove unmatched tokens from the response.
        messages.append({"role": "assistant", "content": Answer})  # Add the AI's response to messages.
        return Answer

    Topic = Topic.replace("Content ", "")  # Remove "Content" from the topic.
    ContentByAI = ContentWriterId(Topic)  # Generate content using AI.

    # Ensure the "Data" directory exists
    os.makedirs("Data", exist_ok=True)

    # Write the content to a file
    file_path = f"Data/{Topic.lower().replace(' ', '')}.txt"
    with open(file_path, "w") as file:
        file.write(ContentByAI)  # Write the content to the file.

    OpenMessage(file_path)  # Open the file in Notepad.
    return True  # Indicate success.

# Function to search for a topic on YouTube.
def YouTubeSearch(Topic):
    url_search = f"https://www.youtube.com/results?search_query={Topic}"  # Construct the YouTube search URL.
    webbrowser.open(url_search)  # Open the search URL in a web browser.
    return True  # Indicate success.

# Function to play a video on YouTube.
def PlayYoutube(query):
    playonyt(query)  # Use pywhatkit's playonyt function to play the video.
    return True  # Indicate success.

# Function to open an application or a relevant webpage.
def OpenApp(app, sess=requests.Session()):
    try:
        # Try to open the app using AppOpener
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True
    except Exception as e:
        print(f"Failed to open {app} using AppOpener: {e}")
        print("Attempting to open using subprocess...")

        # Fallback to subprocess for opening apps
        app_mapping = {
            "notepad": "notepad.exe",
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            # Add more app mappings as needed
        }

        if app.lower() in app_mapping:
            try:
                subprocess.Popen(app_mapping[app.lower()])
                return True
            except Exception as subprocess_error:
                print(f"Failed to open {app} using subprocess: {subprocess_error}")
        else:
            print(f"No mapping found for app: {app}")

        return False

# Function to close an application.
def CloseApp(app):
    if "chrome" in app:
        pass  # Skip if the app is Chrome.
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)  # Attempt to close the app.
            return True  # Indicate success.
        except:
            return False  # Indicate failure.

# Function to execute system level commands.
def System(command):
    def mute():
        keyboard.press_and_release("volume mute")  # Simulate the mute key press.

    def unmute():
        keyboard.press_and_release("volume mute")  # Simulate the unmute key press.

    def volume_up():
        keyboard.press_and_release("volume up")  # Simulate the volume up key press.

    def volume_down():
        keyboard.press_and_release("volume down")  # Simulate the volume down key press.

    # Execute the system command.
    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    return True  # Indicate success.

# Asynchronous function to translate and execute user commands.
async def TranslateAndExecute(commands: list[str]):
    funcs = []  # List to store asynchronous tasks.
    for command in commands:
        if command.startswith("open "):  # Handle "open" commands.
            if "open it" in command:  # Ignore "open it" commands.
                pass
            elif "open file" == command:  # Ignore "open file" commands.
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))  # Schedule app opening.
                funcs.append(fun)
        elif command.startswith("general "):  # Placeholder for general commands.
            pass
        elif command.startswith("realtime "):  # Placeholder for real-time commands.
            pass
        elif command.startswith("close "):  # Handle "close" commands.
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))  # Schedule app closing.
            funcs.append(fun)
        elif command.startswith("play "):  # Handle "play" commands.
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))  # Schedule YouTube playback.
            funcs.append(fun)
        elif command.startswith("content "):  # Handle "content" commands.
            fun = asyncio.to_thread(Content, command.removeprefix("content "))  # Schedule content creation.
            funcs.append(fun)
        elif command.startswith("google search "):  # Handle Google search commands.
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))  # Schedule Google search.
            funcs.append(fun)
        elif command.startswith("youtube search "):  # Handle YouTube search commands.
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))  # Schedule YouTube search.
            funcs.append(fun)
        elif command.startswith("system "):  # Handle system commands.
            fun = asyncio.to_thread(System, command.removeprefix("system "))  # Schedule system command.
            funcs.append(fun)
        else:
            print(f"No Function Found for {command}")  # Print an error for unrecognized commands.

    results = await asyncio.gather(*funcs)  # Execute all tasks concurrently.

    for result in results:  # Process the results.
        if isinstance(result, str):
            yield result
        else:
            yield result

# Asynchronous function to automate command execution.
async def Automation(commands: list[str]):
    async for result in TranslateAndExecute(commands):  # Transfer and execute commands.
        pass
    return True  # Indicate success.
