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
#root.attributes('-fullscreen', True)

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


myFont = tkFont.Font(size=16)

rowNumber = 0
columnNumber = 0
number = 0

def testThread():
    time.sleep(1)
    print("Test")

def NewWindow(order):
    window = Toplevel()
    window.geometry('150x150')
    newlabel = Label(window, text = "Cocktail Produktion" + order["name"])
    newlabel.pack()

    thread1 = threading.Thread(target = testThread)
    thread1.start()

  
for drink in drinks:

    buttonText = drinks[number]["name"] + "\n("
    for ingredient in drink["ingredients"]:
        if ingredient != drink["ingredients"][0]:
            buttonText += ", "
        buttonText += ingredient["ingredient"]
    buttonText +=")"
    drinkButton = Button(root, text=buttonText, bg="#00ee00", activebackground="#00ee00", command= lambda drink=drink: buttonClicked(drink), width=10)

    drinkButton['font'] = myFont
    drinkButton.grid(row=rowNumber, column=columnNumber, padx=10, pady=10, ipadx=50, ipady=50, sticky="nesw")
    number+=1
    columnNumber+=1


    if(number%3==0):
      rowNumber+=1
      columnNumber = 0


ExitButton = Button(root, font=myFont, text="Exit", bg="#ee0000", activebackground="#ee0000", command=buttonExitClicked)
ExitButton.grid(row= 2, column=2, padx=10, pady=10, ipadx=10, ipady=10, sticky="nesw")
root.mainloop()
