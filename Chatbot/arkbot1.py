#Basic chatbot. Can interact at a low level, display news, and definitions from Wikipedia
#Facts feature not working currently. Not intelligent.

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
#from textblob import TextBlob as tb, Word #TextBlob is making program slow
from datetime import datetime
import re, keyboard, time, json, random, requests, wikipedia as wk

classes = []

data_file = open('intents.json').read()
intents = json.loads(data_file)

for intent in intents['intents']:
    if intent not in classes:
        classes.append(intent)
        
name = input('Enter contact: ')

#Chrome
option = webdriver.ChromeOptions() 
option.add_argument('--user-data-dir=./User_Data') #For default profile
option.add_argument('--disable-extensions')
driver = webdriver.Chrome('C:\Windows\chromedriver.exe',options=option)

driver.get('https://web.whatsapp.com/')
input('Press Enter after scanning QR code/Loading page') #To do: Automate the enter click
#driver.manage().timeouts().implicitlywait(30 timeunit.seconds)
#keyboard.press_and_release('enter')
print("Service started")

user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name)) #Finding target user
user.click()

#General path for the online element. Won't exist if user is offline
online_xpath = '/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[2]/span'
messagebox_xpath = '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[2]/div/div[2]'
sendbtn_xpath = '/html/body/div[1]/div/div/div[4]/div/footer/div[1]/div[3]/button'
#PATH TO CONTACT'S MESSAGES
recdm_xpath = '//span[@aria-label="{}:"]/parent::*//span[@class="_3Whw5 selectable-text invisible-space copyable-text"]'.format(name)

def getResponse(m):
    res = None
    for c in classes:
        if m.casefold() in c['patterns']:
            res = c 
            #found = True
            break
    if (res is not None):
        a = random.choice(res['responses'])
        print(a)
        return a
    else:
        b = random.choice(classes[0]['responses'])
        print(b)
        return b
    
def send(message):
    msg = message 
    msg_box = driver.find_element_by_xpath(messagebox_xpath)
    msg_box.send_keys(msg)  #For sending message in message box
    driver.find_element_by_xpath(sendbtn_xpath).click() #Send button

def send_delay(message, delay):
    msg = message 
    msg_box = driver.find_element_by_xpath(messagebox_xpath)
    msg_box.send_keys(msg)  #For sending message in message box
    time.sleep(delay)
    driver.find_element_by_xpath(sendbtn_xpath).click() #Send button

def google_search(search_string):
    search_string = search_string.replace(' ', '+')  
    

def wiki_search(s):
    s = s.replace("tell me about","")
    send("One sec...")
    summary = wk.summary(s,sentences=2)
    send(summary)
    send("Okay?")

def get_facts():
    send("Getting interesting facts for interesting person")
    url = "https://bestlifeonline.com/world-facts/"
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    facts = soup.findAll(class_='title')
    for f in facts[:5]:
        send(f.text)
    send("Okay?")

def get_news(): 
    send("Hold on, I'm gathering information...")
    url = "https://timesofindia.indiatimes.com/home/headlines"
    page = requests.get(url)
    soup = BeautifulSoup(page.text,'html.parser')
    headline = soup.findAll(class_='w_tle') 
    send("Here's your news")
    count = 0
    for n in headline[:3]:
        count+=1
        send(n.text)
    send("Okay?")

def youtube(s): 
    topic = s.replace("play on yt ", "")
    send("Please wait while I search about %s on YouTube"%topic)
    url = 'https://www.youtube.com/results?q=' + str(topic)
    sc = requests.get(url)
    sctext = sc.text
    soup = BeautifulSoup(sctext,"html.parser")
    try:
        songs = soup.findAll("div",{"class":"yt-lockup-video"})
        song = songs[0].contents[0].contents[0].contents[0]
        songurl = song["href"]
        #time.sleep(2)
        send_delay("Here's a matching video \nhttps://www.youtube.com"+songurl)
        send("Okay?")
    except:
        #time.sleep(2)
        send("Sorry, I couldn't find any video")
    

wiki_qs = ["tell me about", "Tell me about", "What is"]
start_of_conversation = False
def main():
        oldmsg = ""
        prev_exc = ""
        c1 = 0
        send("Greetings!")
        while True:
            try:
                newmsg = driver.find_elements_by_xpath(recdm_xpath) #NOT A string
                #oldmsg = newmsg[length-1].text
                #length = len(newmsg)
                msg = ((newmsg[-1].text).lower()) #Gets text and converts to lower case although unnecessary
                #print("msg: ", msg)
                    
                if msg != oldmsg:
                    
                    if ("tell me about" in msg and "yourself" not in msg) and c1==0:
                        wiki_search(msg)
                        c1+=1

                    #if Word(msg).spellcheck() != 1.0: #Spellchecking not working 
                        #send(Word(msg).correct()+"*?")

                    #elif "fact" or "facts" in msg and c1==0: #spamming
                        #get_facts()
                        #c1+=1

                    elif "news" in msg and c1==0:
                        get_news()
                        c1+=1

                    elif ("play on yt" in msg or "play" in msg) and c1==0: 
                        youtube(msg)
                        c1+=1

                    else:
                        ans = getResponse(msg)
                        send(ans)
                        
                c1=0
                oldmsg = msg
                time.sleep(2)

            except Exception as e:
                if prev_exc is not e:
                    prev_exc = e
                    print(e)
                else: 
                    pass
                
main()
