from datetime import datetime
import pyttsx3
import datetime
import speech_recognition as sr#for voice to text
import wikipedia
import webbrowser
import os #for music and accessing system apps through path
from youtube_search import YoutubeSearch
import urllib.request # for  getting url # pip install youtube
import pprint #for rreadable printing of html texts
import requests
from bs4 import BeautifulSoup, SoupStrainer #for link extractions

from time import sleep # for asking time
import random #for random number
from os import system, name # clearing screen and some other stuffs
import sys
from googleapiclient.discovery import build
import pprint #for systematic readable printing of web page data
import re # for regular expression matching

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# print(voices[1].id)
engine.setProperty('voice', voices[1].id)


def listToString(s):
	str1 = ""
	# traverse in the string
	for ele in s:
		str1 += ele
	# return string
	return str1

def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak(" good morning ! ")
    elif hour >= 12 and hour < 18:
        speak("good  afternoon ! ")
    else:
        speak("good  evening !")

    # speak(" hii !  i'm anshu ! how  u  remembered  me ?  oh!   i think u need some help?  ")
    speak("how can i help you")



#google search function
my_api_key = "AIzaSyDqnPdeVN0N547Liacefd0qfTx-ziMQX9A"
my_cse_id = "e5f36f7c25f7c4094"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']
_ = system('cls')



def takeCommand():
    # takes voice input from microphone and returns string input
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.energy_threshold = 200
        r.adjust_for_ambient_noise(source, duration=1)
        r.dynamic_energy_threshold = True
        # print('Listening 23')
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        query = query.lower()
        print(f"U said : {query}\n")
      #  speak(query)
    except Exception as e:
        # print(e)

        print("Say that again please...")
        return "None"
    return query


if __name__ == "__main__":
    wishMe()
    flag=True
    while flag:
         query= takeCommand().lower()
         if 'quit' in query:
            flag=False
            speak('thanks for using me!! im glad to help u! see u again')


        #wikipedia
         if 'wikipedia' in query:

            speak('Searching wikipedia...')
            query=query.replace("wikipedia","")
            print(query)
            results=wikipedia.summary(query,sentences=1)
            speak("According to wikipedia")
            print("According to wikipedia: \n")
            print(results)
            speak(results)
            f=True
            while f:
                speak('Do u want to search more? then just aks me or just say no')
                srch=takeCommand().lower()
                if 'no' in srch:

                    f=False
                else:
                    srch=srch.replace("wikipedia","")
                    print(srch)
                    r=wikipedia.summary(srch,sentences=1)
                    speak("According to wikipedia")
                    print(r)
                    speak(r)
            
                





         #youtube
         elif 'open youtube' in  query:
            speak('opening youtube...')
            srch_key=takeCommand()
            srch_key=srch_key.replace(" ","+")
            html=urllib.request.urlopen("https://www.youtube.com/results?search_query=" + srch_key)
            video_ids=re.findall(r"watch\?v=(\S{11})",html.read().decode())
            k=1
            for id in video_ids: #only first 10 results
                if k==10:
                    break
                k=k+1
                print("https://www.youtube.com/watch?v="+id) #top 10 links links 
            
            webbrowser.open("https://www.youtube.com/watch?v="+video_ids[0]) # only opening first link as it's more relevent usually
            



         #google
         elif 'ok google' in  query:
            
            speak('opening google ')
            #speak('HI ! finally u called me !!   Good to see u!    ask me any thing')
            #ask=takeCommand()
            results = google_search(
                'play its ok not to be ok', my_api_key, my_cse_id, num=10)

            stdoutOrigin=sys.stdout 
            sys.stdout = open("search_res.txt", "w")

            for result in results:
                pprint.pprint(results)
                
            sys.stdout.close()
            sys.stdout=stdoutOrigin


            final_links=[] # store all result
            with open("search_res.txt","r") as file:
                    for line in file:
                        urls = re.findall('link\': \'https?://(?:[-\w..//]|(?:%[\da-fA-F-0-9]{2}))+', line) # regular accepted language
                        urls = list(map(lambda x: x.replace('link\': \'', ''), urls))
                        if(urls):
                            final_links.append(urls)
                        

            print(final_links[0])
            webbrowser.open(listToString(final_links[0]))
            os.remove("search_res.txt")


          #stack overflow ->this can be also done by google one it's fully automated
         elif 'open stack overflow' in  query:
            speak('opening stackoverflow...')
            webbrowser.open("stackoverflow.com")



          #system music
         elif 'play music' in query:
            music_dir='E:\\assistant\\music'
            songs=os.listdir(music_dir)
            print(songs)
            os.startfile(os.path.join(music_dir,random.choice(songs)))
          
          
          #time 
         elif 'what\'s the time' in query:
            strTime =datetime.datetime.now().strftime("%H:%m:%S")
            speak(f"the time is {strTime}")

            

            

