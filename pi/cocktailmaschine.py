from tkinter import *
import tkinter.font as tkFont 
import os
import json
import time
import serial

import threading


config = {
    "p1": "havana",
    "p2": "vodka",
    "p3": "vodka",
    "p4": "gin",
    "p5": "gin",
    "p6": "lemon juice",
    "a1": "tonic water",
    "a2": "ginger beer",
    "a3": "soda",
    "a4": "ginger ale"
}

drinkFile = open("drinks.json", "r")
drinks = json.load(drinkFile)

#ser = serial.Serial("COM3")

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

root = Tk()
#root.config(cursor="none", background="black")
root.geometry("1024x576")
root.wm_title('Cocktail-Maschine')
root.attributes('-fullscreen', True)

  
# Add image file
bg = PhotoImage(file = 'background.gif')
bg = bg.subsample(4,4)

transparent = PhotoImage(file = 'transparent.png')
  
# Show image using label
label1 = Label( root, image = bg)
label1.place(x = 0, y = 0)



Grid.rowconfigure(root, 0, weight=1)
Grid.rowconfigure(root, 1, weight=1)
Grid.rowconfigure(root, 2, weight=1)

Grid.columnconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 1, weight=1)
Grid.columnconfigure(root, 2, weight=1)


def buttonClicked(order):
    print(order["name"])
    for ingredient in order["ingredients"]:
        pump = getPump(ingredient["ingredient"])
        print(" --> " + str(ingredient["amount"]) + ingredient ["unit"] + " " + ingredient["ingredient"] + " (" + str(pump) + ")")
      #get pumps of drink


    NewWindow(order)

def buttonExitClicked():
    print("Programm wird beendet")
    root.quit()

def getPump(neededIngredient):
    list = []
    for pump, ingredient in config.items():
        if(ingredient == neededIngredient):
            list.append(pump)

    return list

def calibrate():
    print("Calibrate")

def tare():
    print("Tare")


myFont = tkFont.Font(size=16)

rowNumber = 0
columnNumber = 0
number = 0

myWindow = 0
isFinished = False
percent = 0

def testThread():
    global percent
    
    for i in range(10):
        percent = percent + 10
        time.sleep(0.2)

    global isFinished 
    isFinished = True
    percent = 0
    
def NewWindow(order):
    window = Toplevel(root)
    window.geometry('150x150')
    label = Label(window, text = "Cocktail Produktion" + order["name"])
    label.pack()

    window.after(100, updateValue, window, label)
    thread1 = threading.Thread(target = testThread)
    thread1.start()

    window.attributes('-fullscreen', True)



def updateValue(window, label):
    print("Check finisehd")
    global isFinished 
    if isFinished:
        window.destroy()
        print("Finsehd true")
        isFinished = False
    else:
        labelText = "Percent " + str(percent)
        label.configure(text=labelText)
        window.after(100, updateValue, window, label)
        print("Finsehd false")

def SettingsWindow():
    window = Toplevel()
    window.geometry("1024x576")
    window.wm_title('Settings')
    #root.attributes('-fullscreen', True)

    Grid.rowconfigure(window, 0, weight=1)
    Grid.rowconfigure(window, 1, weight=1)

    Grid.columnconfigure(window, 0, weight=1)
    Grid.columnconfigure(window, 1, weight=1)


    CalibrateButton = Button(window, font=myFont, text="Calibrate", bg="#ee0000", activebackground="#ee0000", command=calibrate)
    CalibrateButton.grid(row= 0, column=0, padx=10, pady=10, ipadx=50, ipady=50, sticky="nesw")

    TareButton = Button(window, font=myFont, text="Tare", bg="#ee0000", activebackground="#ee0000", command=tare)
    TareButton.grid(row= 0, column=1, padx=10, pady=10, ipadx=50, ipady=50, sticky="nesw")
   
    BackButton = Button(window, font=myFont, text="Back", bg="#ee0000", activebackground="#ee0000", command=window.destroy)
    BackButton.grid(row= 1, column=0, padx=10, pady=10, ipadx=50, ipady=50, sticky="nesw")
    ExitButton = Button(window, font=myFont, text="Exit", bg="#ee0000", activebackground="#ee0000", command=buttonExitClicked)
    ExitButton.grid(row= 1, column=1, padx=10, pady=10, ipadx=50, ipady=50, sticky="nesw")

    window.attributes('-fullscreen', True)

for drink in drinks:

    buttonText = drinks[number]["name"] + "\n("
    for ingredient in drink["ingredients"]:
        if ingredient != drink["ingredients"][0]:
            buttonText += ", "
        buttonText += ingredient["ingredient"]
    buttonText +=")"
    
    drinkButton = Button(root, text=buttonText, bg="#ffffff", activebackground="#ffffff", compound="center",command= lambda drink=drink: buttonClicked(drink), width=10)
    drinkButton['font'] = myFont
    drinkButton.grid(row=rowNumber, column=columnNumber, padx=10, pady=10, ipadx=50, ipady=50, sticky="nesw")

    drinkButton['font'] = myFont
    drinkButton.grid(row=rowNumber, column=columnNumber, padx=10, pady=10, ipadx=50, ipady=50, sticky="nesw")
    number+=1
    columnNumber+=1


    if(number%3==0):
      rowNumber+=1
      columnNumber = 0


SettingsButton = Button(root, font=myFont, text="Settings", bg="#ffffff", activebackground="#ffffff", command=SettingsWindow)
SettingsButton.grid(row= 2, column=2, padx=10, pady=10, ipadx=10, ipady=10, sticky="nesw")
#root.attributes('-alpha', 0.5)
root.mainloop()