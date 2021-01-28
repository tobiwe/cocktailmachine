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

drinks = [
    {
    "name":"Gin Tonic",
    "ingredients": [
      { "unit": "cl",
        "amount": 6,
        "ingredient": "gin" },
      { "unit": "cl",
        "amount": 12,
        "ingredient": "tonic water" }
    ]},
    {
    "name":"Caipirinha",
    "ingredients": [
      { "unit": "cl",
        "amount": 6,
        "ingredient": "cachasa" },
      { "unit": "cl",
        "amount": 2,
        "ingredient": "lemon juice" }
    ]
    },
    {
    "name":"Moscow Mule",
    "ingredients": [
      { "unit": "cl",
        "amount": 5,
        "ingredient": "vodka" },
      { "unit": "cl",
        "amount": 15,
        "ingredient": "ginger beer" }
    ]
    },
    {
    "name":"Virgin Gin Tonic",
    "ingredients": [
      { "unit": "cl",
        "amount": 15,
        "ingredient": "soda" },
      { "unit": "cl",
        "amount": 5,
        "ingredient": "lime juce" }
    ]},
    {
    "name":"Vigin Caipirinha",
    "ingredients": [
      { "unit": "cl",
        "amount": 18,
        "ingredient": "ginger ale" },
      { "unit": "cl",
        "amount": 6,
        "ingredient": "maracuja juice" }
    ]
    },
    {
    "name":"Virgin Moscow Mule",
    "ingredients": [
      { "unit": "cl",
        "amount": 20,
        "ingredient": "ginger beer" },
      { "unit": "cl",
        "amount": 5,
        "ingredient": "soda" },
      { "unit": "cl",
        "amount": 3,
        "ingredient": "lemon juce" }
    ]
    }
]

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
