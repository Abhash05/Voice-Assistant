import system_control as sc
import json
import speech_recognition as sr
import webbrowser
import modes_of_assistant as mj
import requests
from modes_of_assistant import aiProcess
from random import randint
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import youtube_func as yf
from system_control import speak

user_name="Your-name"
Assistant_name = "Name-Your-Assistant"
newsapi = "Your-Api-Key"
spotify_client_id = "Your-Client-Id"
spotify_client_secret = "Your-Client-Secret"

# Initialize Spotify clients
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=spotify_client_id, client_secret=spotify_client_secret))

def spotify_search(c):
    results = spotify.search(q=c, limit=1, type='track')
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        track_url = track['external_urls']['spotify']
        webbrowser.open(track_url)
    else:
        speak("Sorry,Unable to retrive the song.")

def google_search(c):
    webbrowser.open(f"https://www.google.com/search?q={c}")

def get_location_info():
    try:
        response = requests.get("https://ipinfo.io/json")
        if response.status_code == 200:
            data = response.json()
            loc = data.get("loc", "")
            city = data.get("city", "")
            country = data.get("country", "")
            if loc:
                lat, lon = map(float, loc.split(","))
                return lat, lon, city, country
            else:
                return None, None, None, None
        else:
            print("Could not retrieve location information.")
            return None, None, None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None, None, None

def get_weather(c):
    lat, lon, city, country = get_location_info()
    if lat is None or lon is None:
        return "Sorry, I couldn't determine your location."
    
    weatherapi = "Your-Api-Key"
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weatherapi}&units=metric"
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json()
        weather_desc = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"The current weather in {city}, {country} is {weather_desc} with a temperature of {temp}°C."
    else:
        search_query = c.replace(" ", "+")
        webbrowser.open(f"https://www.google.com/search?q={search_query}")

def news(c):
    c_new=c.lower().replace("news","").strip()
    response= requests.get(f"https://newsapi.org/v2/everything?q={c_new}&apiKey={newsapi}")
    data = json.loads(response.text)

    if data['status'] == 'ok':
        articles = data['articles']
        article=articles[randint(0,50)]
        speak(article['title'])
        speak(article['description'])
        speak(f"what else do you want around {c_new}?")
        with sr.Microphone() as source:
            print("Respond")
            audio = r.listen(source, timeout=2, phrase_time_limit=1.9)
            command = r.recognize_google(audio)
            if "an article" in command.lower() or "a news article" in command.lower():
                webbrowser.open(article['url'])
            else:
                speak("ok")    
        
    else:
        speak(f"Error fetching news: {data['message']}")

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    
    elif "open youtube" in c.lower():
        webbrowser.open(f"https://www.youtube.com")
    
    elif "open spotify" in c.lower():
        spotify_search(c.replace("open spotify", "").strip())
    
    elif "open instagram" in c.lower():
        webbrowser.open("https://instagram.com")
    
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    
    elif "brightness" in c.lower():
        level = int(''.join(filter(str.isdigit, c)))
        sc.set_brightness(level)
    
    elif "play" in c.lower() or "search" in c.lower() and "on youtube" in c.lower():
        try:
            yf.yt_search(c.lower().replace("play", "").replace("on youtube","").strip())
        except Exception as e:
            print(f"Error: {e}")
    
    elif "news" in c.lower():
        news(c)

    elif "turn off pc" in c.lower() or "shut down" in c.lower():
        sc.turn_off_pc()
    
    elif "restart pc" in c.lower() or "restart computer" in c.lower():
        sc.restart_pc()
    
    elif "sleep pc" in c.lower() or "sleep computer" in c.lower():
        sc.sleep_pc()
        
    elif "pause" in c.lower():
        yf.pause()
    
    elif "resume" in c.lower():
        yf.resume()
    
    elif "full screen" in c.lower():
        yf.full_screen()
    
    elif "short screen" in c.lower():
        yf.short_screen()
    
    elif "skip ad" in c.lower():
        yf.skip_ad()

    elif "friendly chat mode" in c.lower():
        mj.friend_mode()
    
    elif "consultancy mode" in c.lower():
        mj.consultant_mode()
    
    elif "youtube search" in c.lower() or "search on youtube" in c.lower():
        yf.yt_search(c.lower().replace("youtube search", "").strip())
    
    elif "play" in c.lower() and "on spotify" in c.lower():
        spotify_search(c.lower().replace("play", "").replace("on spotify","").strip())
    
    elif "google search" in c.lower() or "search on google" in c.lower():
        google_search(c.lower().replace("google search", "").strip())
    
    elif "weather" in c.lower():
        weather_info = get_weather(c)
        speak(weather_info)
    
    elif "location" in c.lower():
        location_info = get_location_info()
        speak(location_info)
    
    # New Volume Control Commands
    elif "volume up" in c.lower():
        sc.volume_up()
    elif "volume down" in c.lower():
        sc.volume_down()
    elif "mute" in c.lower():
        sc.mute_volume()
    elif "set volume to" in c.lower():
        level = int(''.join(filter(str.isdigit, c)))
        sc.set_volume(level)

    # New Media Control Commands
    elif "play media" in c.lower() or "pause media" in c.lower():
        sc.play_pause_media()
    elif "next track" in c.lower():
        sc.next_track()
    elif "previous track" in c.lower():
        sc.previous_track()

    else:
        output = aiProcess(c)
        if "i don't know" in output.lower() or "i'm not sure" in output.lower():
            speak("I'm not sure about that, but I can find it for you.")
            google_search(c)
        else:
            if output.lower().endswith("want to know more") or output.lower().endswith("can you be more specific") or output.lower().endswith("you"):
                    with sr.Microphone() as source:
                        print("Listening for further details...")
                        speak("What more do you want to know?")
                        audio = r.listen(source, timeout=4, phrase_time_limit=3)
                        command = r.recognize_google(audio)
                        processCommand(command)
            else:
                speak(output)

if __name__ == "__main__":
    print("Recognizing...")
    speak(f"Initializing {Assistant_name}...")
    while True:
        r = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening for wake word...")
                audio = r.listen(source, timeout=4, phrase_time_limit=2)
            word = r.recognize_google(audio)
            if word.lower() == Assistant_name:
                reply = aiProcess(word)
                result=mj.greet()
                if result is None:
                    speak(reply)
                else:
                    speak(f"{result} {user_name},{reply}")
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = r.listen(source, timeout=4, phrase_time_limit=3)
                    command = r.recognize_google(audio)
                    if "exit" in command.lower():
                        speak(f"{Assistant_name} has terminated...")
                        print("You have exited...")
                        break 
                    processCommand(command)
        except Exception as e:
            print(f"Error: {e}")
