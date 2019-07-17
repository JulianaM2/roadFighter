# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 09:39:33 2019

@author: jumunoz
"""
import tkinter as tk
import roadFighter as rf
from PIL import ImageTk, Image

#Function to replace the window with the gameover menu
def gameOverWindow (points):
      
    gameOver = tk.Tk() #Start a new window named gameover
    gameOver.title('Gameover') 
    gameOver.geometry('200x250') 
    gameOver.iconbitmap('carIcon.ico')
    
    #Background of the window
    img = ImageTk.PhotoImage(Image.open('road.png'))
    tk.Label(gameOver, image = img).pack()
    
    tk.Label(gameOver, text = 'GAMEOVER', font = ('Bahnschrift Light Condensed', 25), 
             bg = 'gray45', fg = 'white').place(x = 42, y = 20)
    tk.Label(gameOver, text = 'YOU GOT: ' + str(points) +' POINTS', bg = 'gray45', 
             font = ('Bahnschrift Light Condensed', 13), fg = 'white').place(x = 40, y = 90)
    tk.Button(gameOver, text = 'PLAY', command = lambda:play(gameOver), bd = 3, padx = 10,
              font = ('Bahnschrift Condensed', 12), bg = '#93b5b3').place(x = 40, y = 150)
    tk.Button(gameOver, text='EXIT', command = gameOver.destroy, bd = 3, padx = 12,
              font = ('Bahnschrift Condensed', 12), bg = '#93b5b3').place(x = 110, y = 150)
    gameOver.mainloop() 
#End gameOverWindow

#Function to show the main menu
def mainMenu():
  
    mainMenu = tk.Tk()
    mainMenu.title('Welcome')
    mainMenu.geometry('200x250')
    mainMenu.iconbitmap('carIcon.ico')
                
    img = ImageTk.PhotoImage(Image.open('road.png'))
    tk.Label(mainMenu, image = img).pack()
 
    tk.Label(mainMenu, text = 'WELCOME', font = ('Bahnschrift Light Condensed', 25),
             bg = 'gray45', fg = 'white' ).place(x = 48,y = 30)
    tk.Button(mainMenu, text = 'PLAY', command = lambda:play(mainMenu), bd = 3, padx = 10,
              font = ('Bahnschrift Condensed', 12), bg = '#93b5b3').place(x = 40, y = 150)
    tk.Button(mainMenu, text='EXIT', command = mainMenu.destroy, bd = 3, padx = 12,
              font = ('Bahnschrift Condensed', 12), bg = '#93b5b3').place(x = 110, y = 150)
    mainMenu.mainloop()
#End mainMenu

#Function to start the game
def play(page):
    page.destroy()
    rf.playRoadFighter()
#End play  