A Personal AI Voice Assistant

core.py is the chatbot implemented without deep learning. core-with-ai.py implements a very simple neural network with Tensorflow and Tflearn, trained on the prompts and responses in the intents.json file. Certain functions of both chatbots are limited to Windows, for example opening Notepad. 

"Jarvis" can do the following:

1. Get the weather
2. Get the next event on your Google Calendar using the Calendar API
3. Note things on Notepad (Windows only)
4. Open (valid) URLs (example: www.instagram.com, www.facebook.com, www.wikipedia.org, etc.)
5. Search Google for some query
6. Play songs from Spotify (provided you have Premium)

Coming soon:
1. Google Docs support
2. Google Calendar Events addition feature
3. Getting the news
4. Sending emails
