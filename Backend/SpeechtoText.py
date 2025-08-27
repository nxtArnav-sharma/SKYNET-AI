from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import dotenv_values
import os
import mtranslate as mt

# Load environment variables from the .env file
env_vars = dotenv_values(".env")

# Get the input language setting from environment variables
InputLanguage = env_vars.get("InputLanguage", "en")  # Default to English if not found

# Define HTML for the speech recognition interface
HtmlCode = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Speech Recognition</title>
</head>
<body>
    <button id="start">Start</button>
    <button id="end">Stop</button>
    <div id="output"></div>
    <script>
        var recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = '{InputLanguage}';
        document.getElementById('start').onclick = function() {{
            recognition.start();
        }};
        recognition.onresult = function(event) {{
            document.getElementById('output').innerText = event.results[0][0].transcript;
        }};
        document.getElementById('end').onclick = function() {{
            recognition.stop();
        }};
    </script>
</body>
</html>
"""

# Ensure the Data directory exists
os.makedirs("Data", exist_ok=True)

# Write HTML code to a file
html_file_path = os.path.abspath("Data/Voice.html")
with open(html_file_path, "w", encoding="utf-8") as f:
    f.write(HtmlCode)

# Get the current working directory
current_dir = os.getcwd()

# Chrome WebDriver options
chrome_options = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.6943.126 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_argument("--use-fake-ui-for-media-stream")
chrome_options.add_argument("--use-fake-device-for-media-stream")
chrome_options.add_argument("--headless=new")  # Ensure it runs without GUI

# Ensure correct ChromeDriver version (133.0.6943.126)
service = Service(ChromeDriverManager(driver_version="133.0.6943.126").install())

# Initialize WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# Define path for temporary files
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
os.makedirs(TempDirPath, exist_ok=True)  # Ensure directory exists

# Function to set assistant's status
def SetAssistantStatus(Status):
    with open(os.path.join(TempDirPath, "Status.data"), "w", encoding="utf-8") as file:
        file.write(Status)

# Function to modify query punctuation and formatting
def QueryModifier(Query):
    new_query = Query.lower().strip()
    query_words = new_query.split()
    question_words = ["how", "what", "who", "where", "when", "why", "which", "whose", "whom", "can you", "what’s", "where’s", "how’s", "can you"]

    # Add a question mark if it's a question
    if any(word + " " in new_query for word in question_words):
        if query_words[-1][-1] not in [".", "?", "!"]:
            new_query += "?"
    else:
        if query_words[-1][-1] not in [".", "?", "!"]:
            new_query += "."

    return new_query.capitalize()

# Function to translate text into English
def UniversalTranslator(Text):
    english_translation = mt.translate(Text, "en", "auto")
    return english_translation.capitalize()

# Function to perform speech recognition
def SpeechRecognition():
    driver.get("file://" + html_file_path)

    # Start speech recognition
    driver.find_element(By.ID, "start").click()

    while True:
        try:
            Text = driver.find_element(By.ID, "output").text
            if Text:
                # Stop recognition
                driver.find_element(By.ID, "end").click()

                if "en" in InputLanguage.lower():
                    return QueryModifier(Text)
                else:
                    SetAssistantStatus("Translating...")
                    return QueryModifier(UniversalTranslator(Text))
        except Exception:
            pass

# Main loop for speech recognition
if __name__ == "__main__":
    try:
        while True:
            recognized_text = SpeechRecognition()
            print(recognized_text)
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        driver.quit()
        print("ChromeDriver closed.")
