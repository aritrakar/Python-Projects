from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import keyboard, winsound

name = input('Enter contact: ')

#Chrome
option = webdriver.ChromeOptions() 
option.add_argument('--user-data-dir=./User_Data') #For default profile

#option.add_argument('--user-data-dir=C:\\Users\\Aritra Kar\\AppData\\Local\\Google\\Chrome\\User Data\\Profile 2') #Not working
#option.add_argument('--profile-directory=Profile 2') #Error

option.add_argument('--disable-extensions')
driver = webdriver.Chrome('C:\Windows\chromedriver.exe',options=option)

#Firefox. Error
#option = webdriver.FirefoxOptions()
#option.add_argument('--user-data-dir=./UserData')
#driver = webdriver.Firefox('C:\\Windows\\geckodriver.exe',options=option) #Can't find directory for some reason

driver.get('https://web.whatsapp.com/')
input('Press Enter after scanning QR code/Loading page') #To do: Automate the enter click
print("Service started")

user = driver.find_element_by_xpath('//span[@title = "{}"]'.format(name)) #Finding target user
user.click()

#General path for the online element. Won't exist if user is offline
xpath = '/html/body/div[1]/div/div/div[4]/div/header/div[2]/div[2]/span'

st = None

startTime = 0
endTime = 0
duration = 0
hadComeOnline = False

#Main loop

while True:
        file = open('record.txt', 'a')
        try:
            st = WebDriverWait(driver, 0.1).until(EC.presence_of_element_located((By.XPATH, xpath)))
            if(st is not None):
                try: 
                    online = "online" in st.get_attribute("title")
                    t = datetime.now()               
                    if(online and not hadComeOnline):     
                        winsound.Beep(1500, 250)
                        startTime = t
                        hadComeOnline = True
                        out = "{n} is online at {time}".format(n=name, time=t)
                        print(out)
                        file.write(out+ "\n")
                except:
                    st = None
                    pass

        except TimeoutException:
            st = None #???
            if((st is None) and hadComeOnline is True):
                winsound.Beep(1000, 250)
                temp = "{n} went offline at {time}".format(n=name, time=t)
                print(temp)
                file.write(temp+ "\n")
                endTime = datetime.now()
                duration = endTime - startTime
                temp2 = "Duration: {d}".format(d=duration) 
                print(temp2)
                file.write(temp2 + "\n")
                file.write("\n")
                file.close()
                hadComeOnline = False
