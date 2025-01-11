from openai import OpenAI
from system_control import speak
import speech_recognition as sr
import requests
from datetime import datetime

r= sr.Recognizer()
stored_search_data=""
count=0

def greet():
    global count

    D={1:"Good,Morning", 2:"Good,Aftenoon", 3:"Good,Evening"}

    current_time = int(datetime.now().strftime("%H"))

    if int(str(current_time)[0])==0:
        current_time=int(str(current_time)[1])

    prev_time=current_time

    current_time=int(datetime.now().strftime("%H"))

    if int(str(current_time)[0])==0:
        current_time=int(str(current_time)[1])

    if prev_time!=current_time:
        count=0

    if count==0:
        count+=1
        if current_time in range(12):
            return D[1]
        elif current_time in range(12,17):
            return D[2]
        else:
            return D[3]

def aiProcess(c):
    client = OpenAI(
        api_key="Your-Api-key"
    )
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": f"You are a virtual assistant named Jarvis, skilled in general tasks like Alexa and Google Cloud.keep it short.Generate unique responses.If {c} is jarvis don't give hello in response."},
            {"role": "user", "content": c}
        ]
    )

    return completion.choices[0].message.content

def google_search_api(query):
    api_key = "Add-Your-key"  # Replace with your actual SerpAPI key
    url = f"https://serpapi.com/search.json?q={query}&api_key={api_key}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        results = []
        for result in data.get("organic_results", []):
            results.append(result.get("snippet", ""))
        
        if results:
            merged_results = " ".join(results)
            return merged_results
        else:
            speak("Sorry, I couldn't find any relevant information.")
    else:
        speak("Sorry, I couldn't retrieve the information from Google.")

def friend_mode():
    speak("Friendly chat mode has been activated.")
    speak("Initiate the chat by saying something.")
    while True:
        try:
            with sr.Microphone() as source:
                print("Give your reponse.")
                audio = r.listen(source, timeout=4, phrase_time_limit=3)
                command = r.recognize_google(audio)
                if "exit" in command.lower():
                    speak("You have exited friendly chat mode...")
                    break
        except sr.exceptions.UnknownValueError as e:
            continue

        client=OpenAI(
            api_key="Add-Your-key"
        )
        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "you are a person whose is my bestfriend response like you are having a chat with me the next response shall be the reply. keep it short."},
                {"role": "user", "content":command}
            ]
        )
        speak(completion.choices[0].message.content)

def consultant_mode():
    speak("Consultancy chat mode has been activated.")
    speak("Around which topic you want consultancy?")
    with sr.Microphone() as source:
        print("Speak the topic of consultance.")
        audio = r.listen(source, timeout=4, phrase_time_limit=3)
        command = r.recognize_google(audio)
    
    search_data=google_search_api(command.lower().strip())
    global stored_search_data

    try:
        if search_data in stored_search_data:
            speak("I have stored imformation about it.You can now ask me questions about it.")
        else:
            stored_search_data+=search_data
            speak("I have gathered the information. You can now ask me questions about it.")
    except Exception as e:
        print(e)

    while True:
        try: 
            with sr.Microphone() as source:
                print("Give your reponse.")
                audio = r.listen(source, timeout=4, phrase_time_limit=3)
                command = r.recognize_google(audio)
                if "exit" in command.lower():
                    speak("You have exited Consultant chat mode...")
                    break
                elif stored_search_data:
                    response = aiProcess(f"Based on the information {stored_search_data} respond to {command}.")
                    speak(response)
        except sr.exceptions.UnknownValueError as e:
            continue
