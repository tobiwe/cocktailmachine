from tkinter import *
import tkinter.font as tkFont
import os
import json
import time
import serial

import threading

def orderButtonClicked(order):
    openPrductionWindow(order)


def commandButtonClicked():
    openCommandWindow()


def exitButtonClicked():
    sendCommand("1 2 0 0 0")
    ser.close()
    root.quit()

def interruptButtonClicked():
    global interrupt
    interrupt = True
    interruptButton.configure(state="disabled")
    sendString("interrupt")


def refillButtonClicked(window):
    sendString("done")
    global refill
    refill = False

    global refillWindowOpen
    refillWindowOpen = False

    window.destroy()

def pumpButtonClicked():
    window = Toplevel()
    window.geometry("1024x576")
    window.resizable(0, 0)
    window.wm_title('Pump')
    window.attributes('-fullscreen', True)

    Grid.rowconfigure(window, 0, weight=1)
    Grid.rowconfigure(window, 1, weight=1)
    Grid.rowconfigure(window, 2, weight=1)
    Grid.rowconfigure(window, 3, weight=1)
    Grid.rowconfigure(window, 4, weight=1)
    Grid.rowconfigure(window, 5, weight=1)
    Grid.rowconfigure(window, 6, weight=1)
    Grid.rowconfigure(window, 6, weight=1)
    Grid.rowconfigure(window, 7, weight=1)
    Grid.rowconfigure(window, 8, weight=1)
    Grid.rowconfigure(window, 9, weight=1)
    Grid.rowconfigure(window, 10, weight=1)


    Grid.columnconfigure(window, 0, weight=1)
    Grid.columnconfigure(window, 1, weight=1)
    Grid.columnconfigure(window, 2, weight=1)
    Grid.columnconfigure(window, 3, weight=1)


    for i in range(0,10):

        TextLabel = Label(window, font=myFont, text="Motor "+str(i))

        Forward = Button(window, font=myFont, text="Forward",
                                bg="#ee0000", activebackground="#ee0000", command=lambda i=i: sendCommand("2 " + str(i) + " 255"))
        Backward = Button(window, font=myFont, text="Backward",
                                bg="#ee0000", activebackground="#ee0000", command=lambda i=i: sendCommand("2 " + str(i) + " -255"))
        Stop = Button(window, font=myFont, text="Stop",
                                bg="#ee0000", activebackground="#ee0000", command=lambda i=i: sendCommand("2 " + str(i) + " 0"))

        TextLabel.grid(row=i, column=0, padx=10, pady=10,  ipadx=50, ipady=50, sticky="nesw")

        Forward.grid(row=i, column=1, padx=10, pady=10,  ipadx=50, ipady=50, sticky="nesw")

        if(i<6):
            Backward.grid(row=i, column=2, padx=10, pady=10,  ipadx=50, ipady=50, sticky="nesw")
        Stop.grid(row=i, column=3, padx=10, pady=10,  ipadx=50, ipady=50, sticky="nesw")


    BackButton = Button(window, font=myFont, text="Back", bg="#ee0000",
                        activebackground="#ee0000", command=window.destroy)
    BackButton.grid(row=10, column=0, padx=10, pady=10,
                    ipadx=50, ipady=50, sticky="nesw")

    window.attributes('-fullscreen', True)

def addPassword(value):
    global password
    password+= value    

def checkPassword():
    global password
    if(password == "300512"):
        password = ""
        settingsButtonClicked()
    else:
        password = ""

def passwordWindow():
    passwordWindow = Toplevel()
    passwordWindow.geometry("1024x576")
    passwordWindow.resizable(0, 0)
    passwordWindow.wm_title('Password')
    passwordWindow.attributes('-fullscreen', True)

    Grid.rowconfigure(passwordWindow, 0, weight=1)
    Grid.rowconfigure(passwordWindow, 1, weight=1)
    Grid.rowconfigure(passwordWindow, 2, weight=1)
    Grid.rowconfigure(passwordWindow, 3, weight=1)

    Grid.columnconfigure(passwordWindow, 0, weight=1)
    Grid.columnconfigure(passwordWindow, 1, weight=1)
    Grid.columnconfigure(passwordWindow, 2, weight=1)

    number = 1
    for i in range (0,3):
        for j in range (0,3):
            NumberButton = Button(passwordWindow, font=myFont, text=number,
                             bg="#ee0000", activebackground="#ee0000",command=lambda number=number: addPassword(str(number)))
            NumberButton.grid(row=i, column=j, padx=10, pady=10,
                         ipadx=50, ipady=50, sticky="nesw")
            number = number + 1

    NumberButton = Button(passwordWindow, font=myFont, text="0",
                             bg="#ee0000", activebackground="#ee0000", command=lambda: addPassword("0"))
    NumberButton.grid(row=3, column=0, padx=10, pady=10,
                         ipadx=50, ipady=50, sticky="nesw")

    OkButton = Button(passwordWindow, font=myFont, text="Ok", bg="#ee0000",
                        activebackground="#ee0000", command=checkPassword)
    OkButton.grid(row=3, column=1, padx=10, pady=10,
                    ipadx=50, ipady=50, sticky="nesw")

    BackButton = Button(passwordWindow, font=myFont, text="Back", bg="#ee0000",
                        activebackground="#ee0000", command=passwordWindow.destroy)
    BackButton.grid(row=3, column=2, padx=10, pady=10,
                    ipadx=50, ipady=50, sticky="nesw")


def settingsButtonClicked():
    window = Toplevel()
    window.geometry("1024x576")
    window.resizable(0, 0)
    window.wm_title('Settings')
    root.attributes('-fullscreen', True)

    Grid.rowconfigure(window, 0, weight=1)
    Grid.rowconfigure(window, 1, weight=1)

    Grid.columnconfigure(window, 0, weight=1)
    Grid.columnconfigure(window, 1, weight=1)
    Grid.columnconfigure(window, 2, weight=1)

    CalibrateButton = Button(window, font=myFont, text="Calibrate",
                             bg="#ee0000", activebackground="#ee0000", command=calibrate)
    CalibrateButton.grid(row=0, column=0, padx=10, pady=10,
                         ipadx=50, ipady=50, sticky="nesw")
    TareButton = Button(window, font=myFont, text="Tare",
                        bg="#ee0000", activebackground="#ee0000", command=tare)
    TareButton.grid(row=0, column=1, padx=10, pady=10,
                    ipadx=50, ipady=50, sticky="nesw")

    CommandButton = Button(window, font=myFont, text="Command", bg="#ee0000",
                           activebackground="#ee0000", command=commandButtonClicked)
    CommandButton.grid(row=0, column=2, padx=10, pady=10,
                       ipadx=50, ipady=50, sticky="nesw")

    BackButton = Button(window, font=myFont, text="Back", bg="#ee0000",
                        activebackground="#ee0000", command=window.destroy)
    BackButton.grid(row=1, column=0, padx=10, pady=10,
                    ipadx=50, ipady=50, sticky="nesw")

    PumpButton = Button(window, font=myFont, text="Pumpen", bg="#ee0000",
                        activebackground="#ee0000", command=pumpButtonClicked)
    PumpButton.grid(row=1, column=1, padx=10, pady=10,
                    ipadx=50, ipady=50, sticky="nesw")

    ExitButton = Button(window, font=myFont, text="Exit", bg="#ee0000",
                        activebackground="#ee0000", command=exitButtonClicked)
    ExitButton.grid(row=1, column=2, padx=10, pady=10,
                    ipadx=50, ipady=50, sticky="nesw")

    window.attributes('-fullscreen', True)


def getPump(neededIngredient):
    list = []
    for pump, ingredient in config.items():
        if(ingredient == neededIngredient):
            list.append(pump)

    return list


def openRefillWindow(ingredient):
    global refillWindowOpen
    refillWindowOpen = True
    refillWindow = Toplevel()
    refillWindow.geometry("1024x576")
    refillWindow.attributes('-fullscreen', True)
    refillWindow.resizable(0, 0)
    refillWindow.wm_title('Refill')

    refillCanvas = Canvas(refillWindow, width=1024,
                          height=576, highlightthickness=0)
    backgrouundCanvas = refillCanvas.create_image(
        0, 0, anchor="nw", image=buttler)
    refillCanvas.place(x=0, y=0)
    refillCanvas.create_image((512, 288), image=info)

    heading = refillCanvas.create_text(
        512, 200, text="Butler", font=headingFont, fill="white")
    label = refillCanvas.create_text(
        512, 320, text="Ohhh - " + ingredient["ingredientText"] + " leer!\nRuf schnell den Cocktail-Butler.\nEr kann dir helfen!\n",  font=myFont, fill="white", justify=CENTER)

    refillButton = Button(refillWindow, font=myFont, text="Weiter geht's!", bg="#ee0000", foreground="white",
                          activebackground="#ee0000", command=lambda refillWindow=refillWindow: refillButtonClicked(refillWindow))
    refillButton.place(x=512, y=420, anchor=CENTER)


def openPrductionWindow(order):

    global interrupt
    interrupt = False

    #sendCommand("1 2 0 0 0")
    productionWindow = Toplevel()
    productionWindow.geometry('1024x576')
    productionWindow.resizable(0, 0)
    productionWindow.focus_force()

    global productionCanvas
    productionCanvas = Canvas(
        productionWindow, width=1024, height=576, highlightthickness=0)
    productionCanvas.create_image(0, 0, anchor="nw", image=production)
    productionCanvas.place(x=0, y=0)

    productionCanvas.create_image((512, 288), image=info)

    heading = productionCanvas.create_text(
        512, 200, text="Es werde", font=headingFont, fill="white")
    drink = productionCanvas.create_text(
        512, 250, text=order["name"], font=headingFont, fill="white")
    process = productionCanvas.create_text(
        512, 350, text="Gleicht geht'los!", font=headingFont, fill="white")

    global interruptButton
    interruptButton = Button(productionWindow, state="disabled", font=myFont, text="Abbrechen", bg="#ee0000", foreground="white",
                          activebackground="#ee0000", command= interruptButtonClicked)
    interruptButton.place(x=512, y=420, anchor=CENTER)

    productionWindow.after(100, updateValue, productionWindow, process)
    thread = threading.Thread(
        target=updateProductionWindow, args=(order, productionWindow))
    thread.start()
    productionWindow.attributes('-fullscreen', True)


def openCommandWindow():

    commandWindow = Toplevel()
    commandWindow.geometry('1024x576')
    commandWindow.resizable(0, 0)
    commandWindow.focus_force()
    commandWindow.attributes('-fullscreen', True)

    Grid.rowconfigure(commandWindow, 0, weight=1)
    Grid.rowconfigure(commandWindow, 1, weight=1)
    Grid.rowconfigure(commandWindow, 2, weight=1)

    Grid.columnconfigure(commandWindow, 0, weight=1)

    CommandText = Text(commandWindow)
    CommandText.grid(row=0, column=0, padx=10, pady=10,
                     ipadx=50, ipady=50, sticky="nesw")

    SendCommand = Button(commandWindow, font=myFont, text="Send", bg="#ee0000", activebackground="#ee0000",
                         command=lambda CommandText=CommandText: sendCommand(CommandText.get(1.0, "end-1c")))
    SendCommand.grid(row=1, column=0, padx=10, pady=10,
                     ipadx=50, ipady=50, sticky="nesw")

    BackButton = Button(commandWindow, font=myFont, text="Back", bg="#ee0000",
                        activebackground="#ee0000", command=commandWindow.destroy)
    BackButton.grid(row=2, column=0, padx=10, pady=10,
                    ipadx=50, ipady=50, sticky="nesw")


def updateProductionWindow(order, window):
    global percent

    percent = "Gib mir dein Glas"
    weight = 0

    while weight < 400 or weight > 650:
        time.sleep(0.2)
        sendCommand("5 1")
        waitForAnser = True
        answer = receiveCommand()
        weight = float(answer)

    for ingredient in order["ingredients"]:
        if(interrupt):
            break;
        pumps = getPump(ingredient["ingredient"])
        percent = (" Ein bisschen " + ingredient["ingredientText"] + "...")

        amount = ingredient["amount"]
        if len(pumps) == 2:
            amount = amount / 2

        for p in pumps:
            if(interrupt):
                break;

            pumpValue = 0

            if str(p) == 'p1':
                pumpValue = 1
            elif str(p) == 'p2':
                pumpValue = 2
            elif str(p) == 'p3':
                pumpValue = 3
            elif str(p) == 'p4':
                pumpValue = 4
            elif str(p) == 'p5':
                pumpValue = 5
            elif str(p) == 'p6':
                pumpValue = 6
            elif str(p) == 'a1':
                pumpValue = 7
            elif str(p) == 'a2':
                pumpValue = 8
            elif str(p) == 'a3':
                pumpValue = 9
            elif str(p) == 'a4':
                pumpValue = 10

            sendCommand("4 " + str(pumpValue) + " " + str(amount))
            interruptButton.configure(state="normal")

            waitForAnser = True

            while waitForAnser:
                result = receiveCommand()
                if result == "refill":
                    global refill
                    refill = True
                    global refillIngredient
                    refillIngredient = ingredient
                if result == "finish":
                    interruptButton.configure(state="disabled")
                    waitForAnser = False
    percent = "Fertig! Prost!"
    sendCommand("6 5 500 0 255 0")

    weight = 400
    while weight > 100:
        time.sleep(0.2)
        sendCommand("5 1")
        waitForAnser = True
        answer = receiveCommand()
        weight = float(answer)

    sendCommand("1 2 0 0 0")
    sendCommand(showCommand)

    global isFinished
    isFinished = True
    percent = 0


def updateValue(window, process):
    global refill
    global refillIngredient
    global refillWindowOpen
    if refill:
        if refillWindowOpen == False:
            openRefillWindow(refillIngredient)

    global isFinished
    if isFinished:
        window.destroy()
        isFinished = False
    else:
        labelText = str(percent)
        productionCanvas.itemconfig(process, text=labelText)
        window.after(100, updateValue, window, process)

# arduino commands
def calibrate():
    sendCommand("5 3 302.00")


def tare():
    sendCommand("5 2")


def sendString(command):
    ser.write(command.encode())
    ser.write(b'\n')


def sendCommand(command):
    time.sleep(0.1)
    ser.write(b'\x02')
    ser.write(command.encode())
    ser.write(b'\x03')
    ser.flush()
    time.sleep(0.1)

def receiveCommand():
    line = ""
    started = False
    ended = False

    while ended == False:
        for character in ser.read():
            if character == 2:
                started = True
            elif character == 3:
                ended = True
            elif started:
                line += chr(character)

    return line

def createButton(x, y):
    drinkButton = canvas.create_image((x, y), image=transparent)
    label = canvas.create_text(
        (x, y), text=buttonText, font=myFont, fill="white")
    event = '<Button-1>'
    canvas.tag_bind(drinkButton, event, lambda e,
                    mydrink=drink: orderButtonClicked(mydrink))
    canvas.tag_bind(label, event, lambda e,
                    mydrink=drink: orderButtonClicked(mydrink))


config = {
    "p1": "bacardi",
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

showCommand = "6 1 10"

# test or productive environment?
ser = serial.Serial("/dev/ttyACM0", 9600)
#ser = serial.Serial("COM4", 9600)

time.sleep(2)

if os.environ.get('DISPLAY', '') == '':
    os.environ.__setitem__('DISPLAY', ':0.0')

root = Tk()
root.config(cursor="none", background="black")
root.geometry("1024x576")
root.resizable(0, 0)
root.wm_title('Cocktail-Maschine')
root.focus_force()
root.attributes('-fullscreen', True)

# load background image
bg = PhotoImage(file='background.png')
transparent = PhotoImage(file='transparent.png')
info = PhotoImage(file='info.png')
production = PhotoImage(file='production.png')
settings = PhotoImage(file='settings.png')
buttler = PhotoImage(file='buttler.png')


canvas = Canvas(root, width=1024, height=576, highlightthickness=0)
backgrouundCanvas = canvas.create_image(0, 0, anchor="nw", image=bg)

myFont = tkFont.Font(size=22, family="Franklin Gothic Medium")
headingFont = tkFont.Font(size=32, family="Franklin Gothic Medium")

rowNumber = 0
columnNumber = 0
number = 0

myWindow = 0
isFinished = False
percent = 0
refill = False
refillIngredient = ""
refillWindowOpen = False
index = 1

password = ""

for drink in drinks:

    buttonText = drinks[number]["name"]  # + "\n("
 #   for ingredient in drink["ingredients"]:
    #  if ingredient != drink["ingredients"][0]:
    #buttonText += ", "
    #buttonText += ingredient["ingredient"]
   # buttonText +=")"

   # drinkButton = Button(root, text=buttonText, image=transparent,bd=0, compound="center",command= lambda drink=drink: orderButtonClicked(drink))
   # drinkButton['font'] = myFont

    #createButton(204+308*columnNumber, 186+204*rowNumber)
    createButton(194+318*columnNumber, 181+214*rowNumber)

    #drinkButton.grid(row=rowNumber, column=columnNumber, padx=10, pady=10, ipadx=50, ipady=50, sticky="nesw")

    number += 1
    columnNumber += 1

    if(number % 3 == 0):
        rowNumber += 1
        columnNumber = 0

    index += 1

    canvas.place(x=0, y=0)

#SettingsButton = Button(root, font=myFont, text="Settings", image = transparent, command=settingsButtonClicked)
#SettingsButton.grid(row= 2, column=2, padx=10, pady=10, ipadx=10, ipady=10, sticky="nesw")

settingsButton = canvas.create_image((1014, 566), anchor="se", image=settings)
event = '<Button-1>'
canvas.tag_bind(settingsButton, event, lambda e: passwordWindow())
sendCommand(showCommand)

#root.attributes('-alpha', 0.5)
root.mainloop()
