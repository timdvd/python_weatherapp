# Visual imports
import tkinter as tk
from PIL import ImageTk, Image
import requests
# Audio imports
import speech_recognition as sr
import pyaudio
import pyttsx3
import os
import sys

HEIGHT = 640
WIDTH = 480

# Code for speeach
def talk(words):
    '''
    Function to make bot speak 
    '''
    engine = pyttsx3.init()
    engine.say(words)
    engine.runAndWait()
def listen():
    '''
    Function that listen user and returns information
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source:
        talk('Speak')
        r.adjust_for_ambient_noise(source, duration = 0.5)
        audio = r.listen(source)
    try:
        com = r.recognize_google(audio).lower()
        entry.delete(0, 'end')
        entry.insert(0, str(com.capitalize()))
        label['text'] = ''
        talk('The city you have chosen is ' + com)
    except sr.UnknownValueError:
        talk('Can\'t get information about the weather please try again')
        com = listen()
    return com
# Function that gets a weather data
def formated(weather):
    ''' 
    Function that format output data
    '''
    try:
        name = weather['name']
        desc = weather['weather'][0]['description']
        temp = weather['main']['temp']
        final =  'City: %s. \nCondition: %s. \nTemperature: %s °C.' % (name,desc,temp)
    except:
        final = 'There is a trouble in getting a weather\ninformation'
    return final
def getWeather(city):
    key = '---------------------------' # your api key here
    url = 'https://api.openweathermap.org/data/2.5/weather'
    parameters = {'APPID': key, 'q': city, 'units': 'Metric'}
    responce = requests.get(url, params=parameters)
    weather = responce.json()
    label['text'] = formated(weather)
    return formated(weather)

def sayWeather():
    text = label['text']
    if text == '':
        talk('No information has been given')
    talk(text)
# Visual part of the app
root = tk.Tk()
root.title('Get weather')
root.resizable(False, False)
# Setting a geometry for the window
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

background_image = ImageTk.PhotoImage(Image.open(".img\\bg.png"))
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1,relheight=1)
# Upper frame with input field and buttons
frame = tk.Frame(root, bg='#B5E7E3',bd=7)
frame.place(relx=0.5,rely=0.1,relwidth=0.8,relheight=0.1,anchor='n')

entry = tk.Entry(frame, font=('Arial',14), bd=0, relief=tk.FLAT, borderwidth=10)
entry.place(relwidth=0.45,relheight=1)

button = tk.Button(frame, bd=1, text='Launch',font=('Arial', 12), command= lambda: getWeather(entry.get()))
button.place(relx=0.5,relheight=1, relwidth=0.27)
# Microphone Button
micro_img = ImageTk.PhotoImage(Image.open(".img\\micro.png"))
micro = tk.Button(frame,image=micro_img, bd=1,command=lambda: getWeather(listen()))
micro.place(relx=0.8,relheight=1, relwidth=0.20)
# Lower frame with some content
lower_frame = tk.Frame(root,bg='#B5E7E3',bd=7,borderwidth=12)
lower_frame.place(relx=0.5,rely=0.25,relwidth=0.8,relheight=0.6,anchor='n')

label = tk.Label(lower_frame, bg='white', font=('Arial', 16), justify='left', anchor="w")
label.place(relwidth=1,relheight=1)
# Quit button
quit_frame = tk.Frame(root, bg='#B5E7E3',bd=7)
quit_frame.place(relx=0.6,relwidth=0.3,relheight=0.075,rely=0.88)

quit_btn = tk.Button(quit_frame, bd=1, text="Quit program", font=('Arial', 12), command = root.quit)
quit_btn.place(relwidth=1,relheight=1)

voice_png = ImageTk.PhotoImage(Image.open(".img\\voice.png"))
talk_frame = tk.Frame(root, bg='#B5E7E3',bd=7)
talk_frame.place(relx=0.1,relwidth=0.2,relheight=0.075,rely=0.88)
talk_btn = tk.Button(talk_frame, bd=1,image = voice_png, text="Say Info", font=('Arial', 12), command = sayWeather)
talk_btn.place(relwidth=1,relheight=1)

root.mainloop()
