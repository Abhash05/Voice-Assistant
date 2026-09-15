Personalized Voice Assistant

A Python-based desktop voice assistant that listens for spoken commands, answers questions using AI and web search, controls media and Windows settings, and retrieves live information such as weather, news, and location.

Platform: Windows. Several system-control features use Windows-specific APIs and commands.

Features

Speech recognition through the system microphone

Text-to-speech responses

Friendly chat and consultancy conversation modes

Google and YouTube search

Spotify track search

Weather, approximate location, and news updates

Quick access to Google, YouTube, Spotify, Instagram, and LinkedIn

Brightness and volume control

Media playback controls: play/pause, next track, and previous track

YouTube controls: pause/resume, full screen, exit full screen, and skip ads

Windows power controls: shut down, restart, and sleep

Project Structure

Voice-Assistant/
├── main.py                 # Main listening loop and command routing
├── modes_of_assistant.py   # AI chat and consultancy modes
├── system_control.py       # Brightness, volume, media, and power controls
├── youtube_func.py         # YouTube search and playback controls
└── README.md

Technologies Used

Python

SpeechRecognition and Google Speech Recognition

pyttsx3

OpenAI API

Google Custom Search / SerpAPI

YouTube Data API

Spotify Web API

OpenWeather API

NewsAPI

PyAutoGUI

Pycaw, comtypes, and screen-brightness-control

Installation

1. Clone the repository

git clone https://github.com/Abhash05/Voice-Assistant.git
cd Voice-Assistant

2. Create and activate a virtual environment

python -m venv .venv
.venv\Scripts\activate

3. Install the dependencies

pip install SpeechRecognition PyAudio pyttsx3 requests openai google-api-python-client spotipy pyautogui pycaw comtypes screen-brightness-control

If PyAudio fails to install, install a wheel compatible with your Python and Windows versions, then rerun the command.

API Configuration

The assistant uses external services that require credentials:

OpenAI

YouTube Data API

Spotify Web API

OpenWeather

NewsAPI

SerpAPI

Do not commit API keys or client secrets to GitHub. Store them in environment variables or a local .env file excluded through .gitignore, and load them in the application at runtime.

Recommended variable names:

OPENAI_API_KEY=your_key
YOUTUBE_API_KEY=your_key
SPOTIFY_CLIENT_ID=your_client_id
SPOTIFY_CLIENT_SECRET=your_client_secret
OPENWEATHER_API_KEY=your_key
NEWS_API_KEY=your_key
SERPAPI_API_KEY=your_key

Usage

Run the main program:

python main.py

Allow microphone access when prompted. The assistant waits for its wake word and then listens for a command.

Example commands:

Open YouTube
Search Python tutorials on Google
Play a song on Spotify
Set volume to 50
Set brightness to 70
What is the weather?
Tell me the news
Friendly chat mode
Consultancy mode

Power commands such as shutdown, restart, and sleep directly affect the computer. Use them carefully.

Current Limitations

Designed primarily for Windows

Requires a working microphone and internet connection

Depends on several third-party APIs and their usage limits

Speech recognition accuracy varies with noise, microphone quality, and pronunciation

Some browser and YouTube controls depend on the active window and screen layout

Future Improvements

Move all credentials to environment-based configuration

Add a requirements.txt file with pinned versions

Add automated tests for command routing

Improve error handling and command validation

Add a graphical interface

Support Linux and macOS where possible

Author

Abhash Kishore Naik

GitHub: Abhash05

License

No license has been added yet. Until a license is provided, the source remains copyrighted by the author and is not automatically available for reuse or redistribution.
