import pyautogui
import time
from googleapiclient.discovery import build
import webbrowser

youtube_api_key = "Your-Api-key"
youtube = build('youtube', 'v3', developerKey=youtube_api_key)

def pause():
    pyautogui.press("k")
    time.sleep(1.2)

def resume():
    pyautogui.press("k")
    time.sleep(1.2)

def full_screen():
    pyautogui.press("f")
    time.sleep(1.2)

def yt_search(c):
    request = youtube.search().list(
        q=c,
        part='snippet',
        type='video',
        maxResults=1
    )
    response = request.execute()
    video_id = response['items'][0]['id']['videoId']
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    webbrowser.open(video_url) 

def short_screen():
    pyautogui.press("esc")
    time.sleep(1.2)

def skip_ad():
    pyautogui.click(1159,699)
    time.sleep(1.2)