# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
from selenium.webdriver.common.keys import Keys
import telegram
import datetime
import os
from dotenv import load_dotenv

####################################################

# Browser options to disable things that are not needed and defaults to accept
# the mic and camera permissions, this is needed to join meetings

option = Options()
option.add_argument("--disable-infobars")
option.add_argument("--disable-extensions")
option.add_argument("--disable-notifications")
option.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2,
    "profile.default_content_setting_values.media_stream_mic": 1,     # 1:allow, 2:block 
    "profile.default_content_setting_values.media_stream_camera": 1,  # 1:allow, 2:block 
})

load_dotenv()
sToken = os.getenv('TELEGRAM_TOKEN')
print(sToken)

bot = telegram.Bot(token=sToken)

updates = bot.get_updates()
chatId = updates[0].message.from_user.id

def getDate():
    dateTime = datetime.datetime.now()
    return dateTime.strftime("%H:%M:%S - %d/%m/%Y")

class Meetbot:

    def __init__(self,username,password,meetlink):

        self.username = username
        self.password = password
        self.meetlink = meetlink

        self.driver = webdriver.Chrome(chrome_options=option, executable_path='chromedriver.exe')

        self.login_gmail()

        
        # login into the gmail account 
        
    def login_gmail(self):

        time.sleep(2)
        
        # getting into the google login page
        self.driver.get('https://accounts.google.com/signin/v2/identifier?flowName=GlifWebSignIn&flowEntry=ServiceLogin')
        time.sleep(2)        
        
        # passing the email id
        self.driver.find_element_by_xpath('//input[@type="email"]').send_keys(self.username)
        time.sleep(2)
            
        next_button1 = self.driver.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button")
        next_button1.click()
        time.sleep(2)
        
        # passing the password
        self.driver.find_element_by_xpath('//input[@type="password"]').send_keys(self.password)       
        time.sleep(2)
            
        next_button2 = self.driver.find_element_by_xpath(
                    "/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button")
        next_button2.click()
        time.sleep(4)

        self.joining_meet()

    # function for joining into the meet
    
    def joining_meet(self):

        # redirecting to the google meet join page
        self.driver.get(self.meetlink)
        time.sleep(2)
        
        # turning off the mic
        mic_off = self.driver.find_element_by_xpath(
                "/html/body/div[1]/c-wiz/div/div/div[9]/div[3]/div/div/div[4]/div/div/div[1]/div[1]/div/div[4]/div[1]/div/div/div")
        mic_off.click()
        time.sleep(1)

        # turning off the camera
        cam_off = self.driver.find_element_by_xpath(
                "/html/body/div[1]/c-wiz/div/div/div[9]/div[3]/div/div/div[4]/div/div/div[1]/div[1]/div/div[4]/div[2]/div/div")
        cam_off.click()
        time.sleep(1)

        # joining the class
        join_button = self.driver.find_element_by_xpath(
                "/html/body/div[1]/c-wiz/div/div/div[9]/div[3]/div/div/div[4]/div/div/div[2]/div/div[2]/div/div[1]/div[1]/span")
        join_button.click()
        time.sleep(20)
        
        # open the chat div
        chat_button = self.driver.find_element_by_xpath(
                "/html/body/div[1]/c-wiz/div[1]/div/div[9]/div[3]/div[10]/div[3]/div[2]/div/div/div[3]/span/button")
        chat_button.click()
        time.sleep(2)

        self.bore_class()

    def bore_class(self):
        
        # if has sent the message
        hasSend = False
        
        # starting people quantity and quantity of people needed to exit
        startPeopleQuant = int(self.driver.find_element_by_xpath(
                "/html/body/div[1]/c-wiz/div[1]/div/div[9]/div[3]/div[10]/div[3]/div[2]/div/div/div[2]/div/div").text)
        
        quitPeopleQuant = int(startPeopleQuant/2)
        
        textoChat = "Entrando na reunião às " + getDate()+"\nCom "+str(startPeopleQuant)+" pessoas\nSairei quando houverem "+str(quitPeopleQuant)+" pessoas."
        bot.send_message(text=textoChat, chat_id=chatId)

        while True:

                try:

                    chat = self.driver.find_element_by_xpath(
                            "/html/body/div[1]/c-wiz/div[1]/div/div[9]/div[3]/div[4]/div[2]/div[2]/div/div[2]").text
                    
                    # transform to lower case
                    chat = chat.lower()
                            
                    # needle to search
                    needle = "presente"
                            
                    # search for needle with regex
                    quantPresentes = len([m.start() for m in re.finditer(r'{}'.format(re.escape(needle)), chat)])
                        
                    # if there's at least 3 needles, sends message                    
                    if (quantPresentes > 3 and hasSend == False):
                        chatBox = self.driver.find_element_by_name("chatTextInput")
                        chatBox.send_keys("presente")
                        time.sleep(1)
                        hasSend = True
                        chatBox.send_keys(Keys.RETURN)
                        
                        textoChat = "Marquei presença às " + getDate()+"."
                        bot.send_message(text=textoChat, chat_id=chatId)
                        
                    # if has sent the message, lookup for the number of people
                    if (hasSend == True):
                        peopleQuant = int(self.driver.find_element_by_xpath(
                                "/html/body/div[1]/c-wiz/div[1]/div/div[9]/div[3]/div[10]/div[3]/div[2]/div/div/div[2]/div/div").text)
                        
                        # if reached the number of people needed to exit, exits
                        if (peopleQuant <= quitPeopleQuant):
                            self.driver.close()
                            textoChat = "Saí da reunião às " + getDate()+"."
                            bot.send_message(text=textoChat, chat_id=chatId)
                            return
                    
                    time.sleep(5)
                    
                except:
                    print("erro!")
                    textoChat = "Erro às " + getDate()+"."
                    bot.send_message(text=textoChat, chat_id=chatId)
                    return

        time.sleep(1)

        self.driver.close()


##################################################################################

# main

if __name__ == "__main__":
           
    username = input("Insira seu E-mail : ")
    
    password = input("Insira sua senha: ")
    
    meetlink = input("Insira o link da reunião do Google Meet: ")
    
    meet_bot = Meetbot(username, password, meetlink)

    print("Fim da sessão")