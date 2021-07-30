from tkinter import *
import tkinter.font as tkFont 
import os
import json
import time
import serial

import threading

## METHODS ##
### GUI ###
def orderButtonClicked(order):
    openPrductionWindow(order)

def exitButtonClicked():
    print("Programm wird beendet")
    ser.close()
    root.quit()

def refillButtonClicked(window):
    sendString("done")
    global refill
    refill = False
    window.destroy()

def settingsButtonClicked():
    window = Toplevel()
    window.geometry("1024x576")
    window.resizable(0, 0)
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
    ExitButton = Button(window, font=myFont, text="Exit", bg="#ee0000", activebackground="#ee0000", command=exitButtonClicked)
    ExitButton.grid(row= 1, column=1, padx=10, pady=10, ipadx=50, ipady=50, sticky="nesw")

    #window.attributes('-fullscreen', True)


def getPump(neededIngredient):
    list = []
    for pump, ingredient in config.items():
        if(ingredient == neededIngredient):
            list.append(pump)

    return list

def openRefillWindow(ingredient):
    window = Toplevel()
    window.geometry('1024x576')
    window.focus_force()

    refillCanvas = Canvas(window, width=1024, height=576, highlightthickness=0)
    backgrouundCanvas =refillCanvas.create_image(0,0,anchor="nw",image=buttler)
    refillCanvas.place(x = 0, y = 0)
    refillCanvas.create_image((512,288), image=info)

    heading = refillCanvas.create_text(512,200,text="Butler", font=headingFont, fill="white")
    label = refillCanvas.create_text(512,320, text = "Hilfe, die Flasche ist leer (" + ingredient["ingredient"] + ")!\nRuf schnell den Cocktail-Butler!\nEr kann dir helfen!\n",  font=myFont, fill="white", justify=CENTER)
 

    #label = Label(window, text = "Hilfe, die Flasche ist leer (" + ingredient["ingredient"] + ")!\n Ruf schnell den Cocktail-Butler!\n Er kann dir helfen!\n", font=myFont)
   # label.pack()

    refillButton = Button(window, font=myFont, text="Flasche aufgefüllt", bg="#ee0000", foreground="white", activebackground="#ee0000", command=lambda window=window: refillButtonClicked(window))
    refillButton.place(x=512,y=420, anchor=CENTER)

def openPrductionWindow(order):
    productionWindow = Toplevel()
    productionWindow.geometry('1024x576')
    productionWindow.resizable(0, 0)
    productionWindow.focus_force()

    global productionCanvas
    productionCanvas = Canvas(productionWindow, width=1024, height=576, highlightthickness=0)
    productionCanvas.create_image(0,0,anchor="nw",image=production)
    productionCanvas.place(x = 0, y = 0)

    productionCanvas.create_image((512,288), image=info)

    heading = productionCanvas.create_text(512,200,text="CocktailProduction", font=headingFont, fill="white")
    drink = productionCanvas.create_text(512,250, text=order["name"], font=headingFont, fill="white" )
    process = productionCanvas.create_text(512,350,text="Start", font=headingFont, fill="white")

    #heading = Label(productionWindow, text = "Cocktail Produktion", font=myFont)
    #drink = Label(productionWindow, text =  order["name"], font=myFont)
    #process = Label(productionWindow, text =  "Start", font=myFont)
    
    #heading.pack()
    #drink.pack()
    #process.pack()

    productionWindow.after(100, updateValue, productionWindow, process)
    thread = threading.Thread(target = updateProductionWindow, args=(order,productionWindow))
    thread.start()
   # window.attributes('-fullscreen', True)


def updateProductionWindow(order, window):
    global percent

    percent = "Waiting for glas"
    weight = 0

    while weight<300:
        sendCommand("5 1")
        waitForAnser = True
        answer = receiveCommand()
        weight = float(answer)
        print("Gewicht: " + str(weight))


    for ingredient in order["ingredients"]:
        pumps = getPump(ingredient["ingredient"])
        percent = (" --> " + str(ingredient["amount"]) + ingredient ["unit"] + " " + ingredient["ingredient"] + " (" + str(pumps) + ")")

        amount = ingredient["amount"]
        if len(pumps) == 2:
           amount = amount / 2

        for p in pumps:

            pumpValue = 0

            if str(p) == 'p1':
                pumpValue=1
            elif str(p)  == 'p2':
                pumpValue =2
            elif str(p)  == 'p3':
                pumpValue =3
            elif str(p) == 'p4':
                pumpValue =4
            elif str(p) == 'p5':
                pumpValue =5
            elif str(p) == 'p6':
                pumpValue =6
            elif str(p) == 'a1':
                pumpValue =7
            elif str(p) == 'a2':
                pumpValue =8
            elif str(p) == 'a3':
                pumpValue =9
            elif str(p) == 'a4':
                pumpValue =10


            sendCommand("4 " + str(pumpValue) + " " + str(amount))

            waitForAnser = True
            
            while waitForAnser:
                print("Wait for answer")
                result = receiveCommand()
                if result == "refill":
                    openRefillWindow(ingredient)
                    global refill
                    refill = True    
                if result == "finish":
                    waitForAnser = False

    percent = "Finished!"
    sendCommand("6 5 500 0 255 0")
    time.sleep(2)
    sendCommand("1 2 0 0 0")
    sendCommand(showCommand)

    global isFinished 
    isFinished = True
    percent = 0

def updateValue(window, process):
    #print("Check finisehd")
    global isFinished 
    if isFinished:
        window.destroy()
       # print("finished true")
        isFinished = False
    else:
        labelText = str(percent)
        #process.configure(text=labelText)
        productionCanvas.itemconfig(process, text=labelText)
        window.after(100, updateValue, window, process)
       # print("finished false")

### arduino commands
def calibrate():
    print("Calibrate")
    sendCommand("5 3 302.00")

def tare():
    print("Tare")
    sendCommand("5 2")

def sendString(command):
    ser.write(command.encode())
    ser.write(b'\n')

def sendCommand(command):
  
    ser.write(b'\x02')
    ser.write(command.encode())
    ser.write(b'\x03')
    time.sleep(0.1)
    print("Send " + command + "...")

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
                line+=chr(character)
           
    print(line)
    return line

def createButton(x, y):
    drinkButton = canvas.create_image((x,y), image=transparent)
    label = canvas.create_text((x,y),text=buttonText, font=myFont, fill="white")
    event = '<Button-1>'
    canvas.tag_bind(drinkButton, event, lambda e, mydrink=drink: orderButtonClicked(mydrink))
    canvas.tag_bind(label, event, lambda e, mydrink=drink: orderButtonClicked(mydrink))


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

showCommand = "6 1 100"

ser = serial.Serial("COM4", 9600)
time.sleep(2)

if os.environ.get('DISPLAY','') == '':
    print('no display found. Using :0.0')
    os.environ.__setitem__('DISPLAY', ':0.0')

root = Tk()
#root.config(cursor="none", background="black")
root.geometry("1024x576")
root.resizable(0, 0)
root.wm_title('Cocktail-Maschine')
root.focus_force()
#root.attributes('-fullscreen', True)
 
# load background image
bg = PhotoImage(file = 'background.png')
transparent = PhotoImage(file = 'transparent.png')
info = PhotoImage(file = 'info.png')
production = PhotoImage(file = 'production.png')
settings = PhotoImage(file='settings.png')
buttler = PhotoImage(file='buttler.png')


canvas = Canvas(root, width=1024, height=576, highlightthickness=0)
backgrouundCanvas =canvas.create_image(0,0,anchor="nw",image=bg)

myFont = tkFont.Font(size=24, family="Franklin Gothic Medium")
headingFont =  tkFont.Font(size=36, family="Franklin Gothic Medium")

rowNumber = 0
columnNumber = 0 
number = 0

myWindow = 0
isFinished = False
percent = 0
refill = False
index = 1

for drink in drinks:

    buttonText = drinks[number]["name"] #+ "\n("
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

    


    number+=1
    columnNumber+=1


    if(number%3==0):
      rowNumber+=1
      columnNumber = 0

    index+=1

    canvas.place(x = 0, y = 0)

#SettingsButton = Button(root, font=myFont, text="Settings", image = transparent, command=settingsButtonClicked)
#SettingsButton.grid(row= 2, column=2, padx=10, pady=10, ipadx=10, ipady=10, sticky="nesw")

settingsButton = canvas.create_image((1014,566), anchor="se", image=settings)
event = '<Button-1>'
canvas.tag_bind(settingsButton, event, lambda e: settingsButtonClicked())
sendCommand(showCommand)

#root.attributes('-alpha', 0.5)
root.mainloop()
