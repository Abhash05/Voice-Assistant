import screen_brightness_control as sbc
import pyttsx3
import pyautogui
import os
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

#Brightness control
def set_brightness(level):
    try:
        sbc.set_brightness(level)
        speak(f"Brightness set to {level} percent.")
    except Exception as e:
        speak(f"Failed to set brightness: {e}")

# Volume control functions
def get_volume_control():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    return cast(interface, POINTER(IAudioEndpointVolume))

def set_volume(level):
    volume = get_volume_control()
    volume.SetMasterVolumeLevelScalar(level / 100, None)
    speak(f"Volume set to {level} percent.")

def volume_up():
    volume = get_volume_control()
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = min(current_volume + 0.1, 1.0)  # Increase by 10%
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    speak("Volume increased.")

def volume_down():
    volume = get_volume_control()
    current_volume = volume.GetMasterVolumeLevelScalar()
    new_volume = max(current_volume - 0.1, 0.0)  # Decrease by 10%
    volume.SetMasterVolumeLevelScalar(new_volume, None)
    speak("Volume decreased.")

def mute_volume():
    volume = get_volume_control()
    volume.SetMute(1, None)
    speak("Volume muted.")


# Media control functions
def play_pause_media():
    pyautogui.press("playpause")
    speak("Toggled play/pause.")

def next_track():
    pyautogui.press("nexttrack")
    speak("Playing next track.")

def previous_track():
    pyautogui.press("prevtrack")
    speak("Playing previous track.")

def turn_off_pc():
    speak("Shutting down the computer in 5 seconds.")
    os.system("shutdown /s /t 5")  # Shuts down the PC after 5 seconds

def restart_pc():
    speak("Restarting the computer in 5 seconds.")
    os.system("shutdown /r /t 5")  # Restarts the PC after 5 seconds

def sleep_pc():
    speak("Putting the computer to sleep in 5 seconds.")
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")  # Puts the PC to sleep