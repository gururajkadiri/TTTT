#!/usr/bin/env python
# coding: utf-8

import numpy as np
import math
import cv2  
import numpy as np
import os
import glob
n=6

def getWinningWays(n):
    matrix=np.zeros((n,n),dtype=int)
    diagonals_1=[]
    diagonals_2=[]
    for num in range(n**2):
        matrix[int(num//n),int(num%n)]=int(num)
    
    winningWays=[]
    for i in range(n):
        winningWays.append(matrix[i,:].tolist())
        winningWays.append(matrix[:,i].tolist())
    for p in range(2*n-1):
        v1=[matrix[p-q][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)]
        v2=[matrix[n-p+q-1][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)]
        if len(v1)>1:
            diagonals_1.append(v1)
        if len(v2)>1:
            diagonals_2.append(v2)
    winningWays=winningWays+diagonals_1+diagonals_2
    return(winningWays)

winning_ways=getWinningWays(n)

def checkValidState(state):
    global n
    if len(state)<n**2:
        state=state+"".join(["O" for i in range(n**2-len(state))])
    s=np.array(list(state))
    c1=len(np.where(s=="F")[0])
    c2=len(np.where(s=="S")[0])
    if c1-c2==0 or c1-c2==1:
        return(True)
    else:
        return(False)


def searchSubstring(state,check):
    b=np.array(list(state))
    substring="".join(b[check])
    return(substring)
    



def checkStateStatus(state):
    global n
    if len(state)<n**2:
        state=state+"".join(["O" for i in range(n**2-len(state))])
    if not checkValidState(state):
        print("Not a valid state")
        print("State is\t"+state)
        return
    global winning_ways
    for check in winning_ways:
            ans=searchSubstring(state,check)
            if ans=="F"*len(check) or ans=="S"*len(check):
                
                return("WIN",check)
    if "O" not in np.array(list(state)):
        return("DRAW",[])
    return("ON",[])


def whoseTurn(s):
    b=np.array(list(s))
    c1=len(np.where(b=="F")[0])
    c2=len(np.where(b=="S")[0])
    if c1==c2:
        return("F")
    if c1-c2==1:
        return("S")
    


def nextMove(state):
    if len(state)<n**2:
        state=state+"".join(["O" for i in range(n**2-len(state))])
    b=np.array(list(state))
    player=whoseTurn(state)
    ind=np.where(b=="O")[0]
    arr=[]
    for i in ind:
        b=np.array(list(state))
        if player=="F":
            b[i]="F"
        if player=="S":
            b[i]="S"
        arr.append("".join(b))
    return(arr)
    



def getBestMove(s):
    if len(s)<n**2:
        s=s+"".join(["O" for i in range(n**2-len(s))])
    ltw=leadingToWin(s)
    if ltw!="NO":
        print("I can win perhaps")
        return(ltw)
    else:
        current_options=nextMove(s)
        np.random.shuffle(current_options)
        arrNotLeadingToWin=[]
        for state in current_options:
            if leadingToWin(state)=="NO":
                arrNotLeadingToWin.append(state)
                cur_opt=nextMove(state)
                for st in cur_opt:
                    if leadingToWin(st)!="NO":
                        return(state)
        print("Just Choosing Randomly now...")
        if len(arrNotLeadingToWin)>0:
            return(np.random.choice(arrNotLeadingToWin))
        else:
            print("A smarter opponent will win now.")
            return(getRandomMove(s))


def getBetterMove(s):
    if len(s)<n**2:
        s=s+"".join(["O" for i in range(n**2-len(s))])
    ltw=leadingToWin(s)
    if ltw!="NO":
        print("I can win perhaps")
        return(ltw)
    else:
        current_options=nextMove(s)
        np.random.shuffle(current_options)
        for state in current_options:
            if leadingToWin(state)=="NO":
                return(state)
        print("A smarter oppenent will win now")
        return(getRandomMove(s))



def leadingToWin(s):
    if len(s)<n**2:
        s=s+"".join(["O" for i in range(n**2-len(s))])
    availableMoves=nextMove(s)
    for state in availableMoves:
        status,check=checkStateStatus(state)
        if status=="WIN":
            return(state)
    return("NO")

def getRandomMove(s):
    availableMoves=nextMove(s)
    return(np.random.choice(availableMoves))


def makeAnimation(title,filename="",wd="",extension="png",loop=True,delay=20):
     import imageio
     if len(filename)==0:
         filename=title
     print("Readying animation...", end=' ')
     import webbrowser
     if len(wd)==0:
            cwd = os.getcwd()
     else:
            #cwd=os.getcwd()+"/"+wd
             cwd=wd
     files=glob.glob(cwd+"/"+title+"@*."+extension)
     files.sort(key=os.path.getmtime)
     #files=[cwd+"/"+"b_"+str(i)+".jpeg" for i in range(37)]
     images=[]
     for file in files:
         images.append(imageio.imread(file))
     imageio.mimsave(filename+".gif", images,duration=0.75)





def removePngs(title):
    print("Deleting pngs and gifs...", end=' ')
    command='rm -rf '+title+"@*.png "
    os.system(command)
    command='rm -rf '+title+".gif "
    os.system(command)
    print("done.")

