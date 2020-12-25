from __future__ import print_function
import os
import re
import sys
import pytz
import time
import json
import random
import pickle
import pyttsx3
import spotipy
import requests
import datetime
import playsound
import subprocess
import webbrowser
from gtts import gTTS
from ai import getResponse
from googlesearch import search
import speech_recognition as sr
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from spotipy.oauth2 import SpotifyOAuth

SCOPES = {"calendar": ['https://www.googleapis.com/auth/calendar.readonly'],
          "docs": ['https://www.googleapis.com/auth/documents.readonly']}
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday", "sunday"]
DAY_EXTENSIONS = ["rd", "th", "st", "nd"]

WEATHER_API_KEY = "REMOVED DUE TO SECURITY REASONS"

SPOTIFY = {"client_id": "REMOVED DUE TO SECURITY REASONS",
           "client_secret": "REMOVED DUE TO SECURITY REASONS",
           "user_id": "REMOVED DUE TO SECURITY REASONS",
           "username": "REMOVED DUE TO SECURITY REASONS",
           "scope": "user-library-read user-read-currently-playing user-read-recently-played " +
           "user-read-playback-state user-top-read user-modify-playback-state",
           "redirect_uri": "https://open.spotify.com/"}

count = 0

### CORE FUNCTIONS ###


def speak2(text):  # Using gTTS. Supports continuous interaction by using 2 files
    global count
    print(text)
    tts = gTTS(text=text, lang="en", tld="com")
    filename = "{c}.mp3".format(c=(count % 2))
    print(count)
    print(filename)
    tts.save(filename)
    playsound.playsound(filename)
    count += 1


def speak(text):  # Using pyttsx3. Better but voice sounds unnatural
    print(text)
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', engine.getProperty('rate')-20)
    engine.say(text)
    engine.runAndWait()
    engine.stop()


def getAudio():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        audio = r.listen(source)
        said = ""
        print("Finished listening")
        try:
            print("Recognising...")
            said = r.recognize_google(audio)
            print("You: ", said)
        except Exception:
            pass
    return said.lower()


def getDate(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    if text.count("tomorrow") > 0:
        return datetime.date.today() + datetime.timedelta(days=1)

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
    if month < today.month and month != -1:
        year += 1

    if day < today.day and month == -1 and day != -1:
        month += 1

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        difference = day_of_week - current_day_of_week
        if difference < 0:
            difference += 7
            if text.count("next") >= 1:
                difference += 7
        return today + datetime.timedelta(difference)

    if month == -1 or day == -1:
        return None
    return datetime.date(month=month, day=day, year=year)


def note():
    speak("What do you want me to write down?")
    note_text = getAudio()
    date = datetime.datetime.now()
    file_name = str(date).replace(":", "-") + "-note.txt"
    with open(file_name, "w") as f:
        f.write(note_text)
    subprocess.Popen(["notepad.exe", file_name])
    speak("I've made a note of that.")


###GOOGLE APIs###

def authenticateGoogle():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    calService = build('calendar', 'v3', credentials=creds)
    docService = build('docs', 'v1', credentials=creds)
    return {"calendar": calService, "docs": docService}


SERVICE = authenticateGoogle()
print("Google authentication completed.")


def createDoc(name, service):  # Docs: Doesn't work as of now
    title = name
    body = {'title': title}
    doc = service.documents().create(body=body).execute()
    speak('Created document with title: {0}'.format(doc.get('title')))


def getEvents(day, service):  # Calendar: Works. Can only get Events. ADD 'CREATE EVENT SUPPORT'
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(),
                                          timeMax=end_date.isoformat(), singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        speak('No upcoming events found.')
    else:
        if (len(events) == 1):
            speak(f"You have 1 upcoming event")
        else:
            speak(f"You have {len(events)} events")
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            if "+05:30" in start:
                start_time = str(start.split("T")[1].split("+")[0])
                proper_time = start_time.split(":")
                if int(proper_time[0]) < 12:
                    start_time += "AM"
                else:
                    start_time = str(
                        int(proper_time[0]) % 12) + str(proper_time[1]) + "PM"
                speak(event["summary"] + " at " + start_time)
            else:
                speak(event["summary"] + ", all day")


def getCal(text):
    date = getDate(text)
    if date:
        getEvents(getDate(text), SERVICE["calendar"])
    else:
        speak("I don't understand")


def getURL(url):  # Alternatively could use the 'validators' package
    url = url.replace("open ", "")
    common_extensions = ['.com', '.net', '.org', '.co', '.in', '.co.in']
    found = False
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)\
            AppleWebKit/537.36 (KHTML, like Gecko) Cafari/537.36'}
    for ext in common_extensions:
        formatted_url = "https://www."+url+ext
        print(formatted_url)
        response = requests.get(formatted_url, headers=headers)
        print(response.status_code)
        if response.status_code == 200:
            webbrowser.open(formatted_url)
            found = True
            break
    if not found:
        speak("Invalid URL")


def getWeather(city):
    # Example: "get the weather in Kolkata" returns just "Kolkata"
    city = city[city.index("in")+3:]
    speak("Fetching weather for "+city)
    URL = f"https://api.openweathermap.org/data/2.5/weather?q={city}" + \
        "&appid=" + WEATHER_API_KEY
    print("URL: ", URL)
    response = requests.get(URL)
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        speak(
            f"Current weather condition in {city} is {data['weather'][0]['description']}")
        speak(
            f"The current temperature is {str(main['temp']-273.15)} degrees Celcius, humidity is {main['humidity']}%")
    else:
        speak("There was an error. Please try again later.")


def googleSearch(text, n):
    if "search for" in text:
        text = text.replace("search for", "")
    elif "look for" in text:
        text = text.replace("look for", "")
    speak("Searching for " + text)
    results = list(search(query=text, tld="com", num=n, stop=n, pause=2))
    random.shuffle(results)
    print("results:", results)
    for i in results:
        print(i)
    speak("Which link do I open?")
    response = getAudio()
    if "first" in response:
        getURL(results[0])
    elif "second" in response:
        getURL(results[1])
    elif "third" in response:
        getURL(results[1])
    elif "fourth" in response:
        getURL(results[1])
    elif response in ["fifth", "last"]:
        getURL(results[1])
    else:
        speak("Invalid input")
    speak("Did that answer your question?")
    ch = getAudio()
    if "yes" in ch:
        speak("Happy to help!")
    else:
        speak("Searching again...")
        googleSearch(text, n+3)


# Spotify
def autheticateSpotify():
    spotifyObject = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY['client_id'],
                                                              client_secret=SPOTIFY['client_secret'],
                                                              redirect_uri="https://www.google.in/",
                                                              scope=SPOTIFY['scope'],
                                                              cache_path=".cache-AnonymousIbex"))
    return spotifyObject


SPOTIFY_OBJECT = autheticateSpotify()
print("Spotify authentication comepleted.")


def getSong(song, spotifyObject):
    devices = spotifyObject.devices()
    if len(devices['devices']) == 0:
        print("No devices found. Initialising device.")
        webbrowser.open("https://open.spotify.com")
        time.sleep(5)
        devices = spotifyObject.devices()
    deviceID = devices['devices'][0]['id']
    print("deviceID: ", deviceID)

    if song.count("play songs by") > 0:
        #Example: "play songs by imagine dragons"
        searchQuery = song.replace("play songs by ", "")
        results = spotifyObject.search(
            searchQuery, type='track,album', limit=None, offset=0)

        try:
            items = results['tracks']['items']
            for item in items:
                spotifyObject.add_to_queue(uri=item['uri'], device_id=deviceID)

            speak(
                f"Playing {items[0]['name']} by {items[0]['artists'][0]['name']}")
            spotifyObject.start_playback(
                uris=[items[0]['uri']], device_id=deviceID)

        except Exception as e:
            print("except: ", str(e))
            speak(f"Sorry, I couldn't play {searchQuery}")

    elif song.count("by") >= 0:
        #Examples: "play pray for me by the weeknd" "play believer"
        searchQuery = song.replace("play", "").replace("by ", "")
        results = spotifyObject.search(
            searchQuery, type='artist,track', limit=1, offset=0)
        try:
            track = results['tracks']['items'][0]
            artist = track['artists'][0]['name']
            track_name = track['name']
            print(f"track['uri']: {track['uri']}")
            print(
                f"Playing {artist} - {track_name}")
            speak(
                f"Playing {track_name} by {artist}")

            spotifyObject.start_playback(
                device_id=deviceID, uris=[track['uri']])
        except:
            speak(f"Sorry, I couldn't play {song}")
    else:
        speak(f"Sorry, I couldn't play {song}")


def togglePlayback(state, spotifyObject):
    if state == "pause":
        spotifyObject.pause_playback(
            device_id=spotifyObject.devices()['devices'][0]['id'])
    elif state == "resume":
        last_played = spotifyObject.current_user_playing_track()
        print("last_played: ", last_played)
        spotifyObject.start_playback(
            device_id=spotifyObject.devices()['devices'][0]['id'], uris=last_played)


def respondToUser(s):
    tag_dict = {
        # "greeting": "",
        # "thanks": "",
        # "asking": "",
        # "options": "",
        # "responses": "",
        # "abuse": "",
        "goodbye": "sys.exit()",
        "weather": "getWeather(s)",
        "calendar": "getCal(s)",
        "note": "note()",
        "document": "",
        "open": "getURL(s)",
        "search": "googleSearch(s, 5)",
        "play_song": "getSong(s, SPOTIFY_OBJECT)",
        "pause_song": "togglePlayback('pause', SPOTIFY_OBJECT)",
        "resume_song": "togglePlayback('resume', SPOTIFY_OBJECT)"}
    (response, tag) = getResponse(s)
    speak(response)
    if tag in tag_dict.keys():
        exec(tag_dict[tag])


def main():
    while True:
        text = getAudio()
        respondToUser(text)


if __name__ == '__main__':
    main()
