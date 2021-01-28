from Tkinter import *
import tkFont

import os
import json

config = {
    "p1": "gin",
    "p2": "cachasa",
    "p3": "lemon juce",
    "a1": "tonic water"
}

drinkFile = open("drinks.json", "r")
drinks = json.load(drinkFile)

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

root = Tk()
root.config(cursor="none", background="black")
root.geometry("1024x576")
root.wm_title('Cocktail-Maschine')
root.attributes('-fullscreen', True)

Grid.rowconfigure(root, 0, weight=1)
Grid.rowconfigure(root, 1, weight=1)
Grid.rowconfigure(root, 2, weight=1)

Grid.columnconfigure(root, 0, weight=1)
Grid.columnconfigure(root, 1, weight=1)
Grid.columnconfigure(root, 2, weight=1)


def buttonClicked():
    print("Button wurde geklickt")

def buttonExitClicked():
    print("Programm wird beendet")
    root.quit()

myFont = tkFont.Font(size=20)

rowNumber = 0
columnNumber = 0
number = 0
for drink in drinks:
    print(drink["name"])
    for ingredient in drink["ingredients"]:
      print(" --> " + str(ingredient["amount"]) + ingredient ["unit"] + " " + ingredient["ingredient"])
    drinkButton = Button(root, text=drinks[number]["name"], bg="#00ee00", activebackground="#00ee00", command=buttonClicked, width=10)
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
