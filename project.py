import random
from random import shuffle
from datetime import datetime
import time
import tkinter
from tkinter import *
from tkinter import messagebox
import PIL
from PIL import ImageTk,Image
import os

#create window
window = Tk()
window.title("Nim Game")
window.geometry('1980x1080')

#global variables
size = 5
Piles = [None] * size
Images = []
LogsEvents = []
#list containg image pathes
Pathes = ["assets/Empty.png",
          "assets/balls1.png",
          "assets/balls2.png",
          "assets/balls3.png",
          "assets/balls4.png",
          "assets/balls5.png",
          "assets/balls6.png",
          "assets/balls7.png"]
WinPath = "assets/YouWin.png"
LosePath = "assets/Gameover.png"
StartWindowPath = "assets/startWin.jpg"
Pag1 = None
Page2 = None
frame5 = None
GameLogs = StringVar()
PileNumber = StringVar()
RemoveCount = StringVar()
logs = None
FinalImage = None

#generates piles in start of the game
def generatePiles():
    for i in range(0, size):
        random.seed(datetime.now())
        num = random.randint(1, 7)
        Piles[i] = num
        time.sleep(0.2)
        
generatePiles()

def create_game():
    Page1.pack_forget()
    Page2.pack()
    
Page1 = Frame(window)
Page1.pack()
img = ImageTk.PhotoImage(Image.open(StartWindowPath))
StartButton = tkinter.Button(Page1,
                   text= "GO!!",
                   image = img,
                   command = create_game,
                   width = 500,
                   height = 500)
StartButton.pack(pady = 100)

Page2 = Frame(window)

#adding title
frame1 = Frame(Page2)
frame1.pack(pady = (50, 0))

welcome_label = Label(frame1,
                        bg = 'lightblue',
                        justify = CENTER,
                        text = "Welcome To Nim Game",
                        font = ("Arial Italic",35, 'italic'))
welcome_label.pack()

#add pile images
frame2 = Frame(Page2)
frame2.pack(pady = (50, 0))

def AddImage(frame, path):
    Photo = ImageTk.PhotoImage(Image.open(path))
    newImage = Label(frame2,
                     image = Photo,
                     bd = 5,
                     relief = "groove")
    newImage.image = Photo
    newImage.pack(side = LEFT)
    Images.append(newImage)
    
for i in range(0, size):
    AddImage(frame2, Pathes[Piles[i]])


#add user input enteries
frame3 = Frame(Page2)
frame3.pack(pady = (50, 0))

pile_number = Label(frame3,
                    text = "Enter Pile Number",
                    font = ("bold"))
pile_number.pack(side = LEFT)
E1 = Entry(frame3,
           bd = 5,
           textvariable = PileNumber)
E1.pack(side = LEFT)

amount_removed = Label(frame3,
                       text = "Enter number of balls to be removed",
                       font = ("bold"))
amount_removed.pack(side = LEFT)
E2 = Entry(frame3,
           bd = 5,
           textvariable = RemoveCount)
E2.pack(side = LEFT)
    
#update pile and image
def UpdatePile(Index, value):
    Piles[Index] -= value
    NewPhoto = ImageTk.PhotoImage(Image.open(Pathes[Piles[Index]]))
    Images[Index].config(image = NewPhoto)
    Images[Index].image = NewPhoto

#get the position contatining the largest number containg bit 2^(largest - 1) on
def GetLargest(largest):
    if largest == 0:
        return -1
    maxx = 0
    pos = -1
    num = pow(2, largest - 1)
    for i in range(0, size):
        if(int(Piles[i]) & int(num)) and (Piles[i] > maxx):
            pos = i
            maxx = Piles[i]
    return pos

#handles logs events
def AddLogEvent(CurrentEvent):
    LogsEvents.append(CurrentEvent)
    GameLogs.set("")
    LogsSize = len(LogsEvents)
    if LogsSize <= 8:
        for LogEvent in LogsEvents:
            GameLogs.set(GameLogs.get() + LogEvent + '\n')
    else:
        for i in range(LogsSize - 8, LogsSize):
            GameLogs.set(GameLogs.get() + LogsEvents[i] + '\n')
            
#handles computer move by computing the nim sum if   
def ComputerPlay():
    print("Before: " + str(Piles))
    Xor = 0
    for i in range(0, size):
        Xor = Xor ^ Piles[i]
    temp = Xor
    largest = 0
    while temp != 0:
        temp = temp // 2
        largest = largest + 1
    pos = GetLargest(largest)
    take = 0
    if pos == -1:
        for i in range(0, size):
            if Piles[i] == 0:
                 continue
            random.seed(datetime.now())
            num = random.randint(1, Piles[i])
            take = num
            pos = i
    else:
        take = Piles[pos] - (Piles[pos] ^ Xor)
    AddLogEvent("computer takes " + str(take) + " balls frome pile " + str(pos + 1))
    UpdatePile(pos, take)
    print("After: " + str(Piles))

#check if all piles are empty
def check():
    for i in range(0, size):
        if Piles[i] != 0:
            return False
    return True

#loading win or lose photo
def LoadFinalImage(PlayerWin):
    Photo = None
    if PlayerWin == True:
        Photo = ImageTk.PhotoImage(Image.open(WinPath))
    else:
        Photo = ImageTk.PhotoImage(Image.open(LosePath))
    FinalImage.config(
        image = Photo)
    FinalImage.image = Photo
    FinalImage.pack()

#user input handling
def ExceptionInvalidInput():
    messagebox.showerror("Error", "Invalid Input")

def user_input():
    global PileNumber, RemoveCount
    try:
        index = int(PileNumber.get()) - 1
        value = int(RemoveCount.get())
    except:
        ExceptionInvalidInput()
        return
        
    if index >= 0 and index < size and value > 0 and value <= Piles[index]:
        frame5.pack(pady = (20, 0))
        AddLogEvent("player takes " + str(value) + " balls frome pile " + str(index + 1))
        PileNumber.set(""), RemoveCount.set("")
        UpdatePile(index, value)
        if check():
            GameLogs.set("")
            logs.pack_forget()
            LoadFinalImage(True)
            return
        ComputerPlay()
        if check():
            GameLogs.set("")
            logs.pack_forget()
            LoadFinalImage(False)
    else:
        ExceptionInvalidInput()

#restart the game
def user_restart():
    global LogsEvents
    generatePiles()
    LogsEvents = []
    PileNumber.set("")
    RemoveCount.set("")
    FinalImage.pack_forget()
    logs.pack()
    frame5.pack_forget()
    for i in range(0, size):
        UpdatePile(i, 0)

#play and restart buttons
frame4 = Frame(Page2)
frame4.pack(pady = (50, 0))

button_enter = Button(frame4,text = "Play",
                      
                      command = user_input,
                      font = ("Arial Italic", 10, 'bold'),
                      width = 10,
                      height = 2)
button_restart = Button(frame4,
                        text = "Restart",
                        command = user_restart,
                        font = ("Arial Italic", 10, 'bold'),
                        width = 10,
                        height = 2)

button_enter.pack(side = LEFT,
                  padx = (0, 50))
button_restart.pack(side = LEFT)

#game logs and final image
frame5 = Frame(Page2)
logs = Label(frame5,
             bg = "white",
             textvariable = GameLogs,
             relief = "groove")
logs.pack()

FinalImage = Label(frame5)

window.mainloop()

