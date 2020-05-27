from tkinter import * 
import tkinter.messagebox
import pickle


import time
from gameBackend import *

global n

gameWindow = Tk()
var = StringVar()
gameWindow.wm_title("TIC TAC TOE 2")
#gameWindow.geometry('{}x{}'.format(100*n, 150*n))
gameWindow.geometry('{}x{}'.format(100*n, 110*n))
gameWindow.configure(bg='white')
gameWindow.resizable(0,0)

turn=True

with open("bestmove.pickle", "rb") as f:
    dicBestMoves = pickle.load(f)
def reset_game():
    global turn
    global var
    global state
    for i in range(n**2):
        arrButtons[i]["state"]="normal"
        arrButtons[i]["bg"]="white"
        arrButtons[i]["text"]=""
    turn=True
    state=""
    var.set("GREEN TURN")

def playAuto():
    global turn
    global n
    global state
    global dicBestMoves
    if state in dicBestMoves.keys():
        print("Reading next move from file")
        best=dicBestMoves[state]
    else:
        best=getBestMove(state)
        
        dicBestMoves[state]=best
    bs=np.array(list(state))
    bb=np.array(list(best))
    i=[i for i in range(n**2) if bs[i]!=bb[i]][0] 

    onClick(i)
def onClick(i):
    for button in arrButtons:
        button["text"]=""
    gameOver=False
    global var
    global myFont 
    global turn
    global n
    global state
    global dicBestMoves
    if len(state)<n**2:
        state=state+"".join(["O" for i in range(n**2-len(state))])
    b=np.array(list(state))
    arrButtons[i]["state"]="disabled"
    arrButtons[i]["text"]='*'
    if turn:
        arrButtons[i]["bg"]="green"
        b[i]="F"
    else:
        arrButtons[i]["bg"]="red"
        b[i]="S"
    state="".join(b)
    status,check=checkStateStatus(state)
    if status=="WIN":
        j=1
        for k in check:
            arrButtons[k]["text"]=str(j)
            j=j+1
        with open("bestmove.pickle", "wb") as f:
                pickle.dump(dicBestMoves,f)
        gameOver=True
        if turn:
            print("GREEN WINS")
            #messagebox.showinfo("Game Over","Green Wins !!!")
            yesno=messagebox.askquestion("Green Wins!!","Play Again?")
        else:
            print("RED WINS")
            #messagebox.showinfo("Game Over","Red Wins !!!")
            yesno=messagebox.askquestion("Red Wins!!","Play Again?")
        if yesno=="no":
            
            gameWindow.destroy()
        else:
            reset_game()
        
    if status=="DRAW":
        print("DRAW")
        yesno=messagebox.askquestion("Game Drawn","Play Again?")
        if yesno=="no":
            gameWindow.destroy()
        else:
            reset_game()
    if not gameOver:
        turn=not turn
        if turn:
            var.set("GREEN TURN")
        else:
            var.set("RED TURN")
            playAuto()
    

    #print("State=\t"+str(state))
    
    

arrButtons=[]
state=""
for i in range(n):
    for j in range(n):
        f = Frame(gameWindow,width=100,height=100)

        B=Button(f, bg="white",text="",height = 100//n,width=100//n,command=lambda k=n*i+j:onClick(k),font=('Helvetica', '30'))

        B["border"] = "0"
        arrButtons.append(B)
        f.rowconfigure(0, weight = 1)
        f.columnconfigure(0, weight = 1)
        f.grid_propagate(0)
        f.grid(row = i, column = j)
        B.grid(sticky = "NWSE")
        
        
        #B.pack()

label = Label( gameWindow, textvariable=var, relief=RAISED,font=("Helvetica", 16),)
label.place(relx = 0.5,  
                   rely = 0.95, 
                   anchor = 'center') 
var.set("GREEN TURN")

gameWindow.mainloop()

