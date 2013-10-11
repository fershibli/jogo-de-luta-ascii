from __future__ import print_function
import msvcrt
import os
import time
import thread
import threading
char=0
personagem_x=10
personagem_y=10
boneco=["  O"," <|\ ","  |"," / \ ","|   |"]

cenario_luta=["_______________________________________________________________________________","|                           _______________________                           |","|                          |  |  |  |  |  |  |  |  |                          |","|                          |__|__|__|__|__|__|__|__|                          |","|                          |  |  |  |  |  |  |  |  |                          |","|        |                 |__|__|__|__|__|__|__|__|                 |        |","|       /|_                                                         _|\       |","|     /  |#            _________________________________            #|  \     |","|   /                 -----------------------------------                 \   |","| /                 _|___________________________________|_                 \ |","| |                -----------------------------------------                | |","| |   ;`|        _|_________________________________________|_        |`:   | |","| |  ;.#|       -----------------------------------------------       |#`:  | |","| | :.##|     _|_______________________________________________|_     |##`: | |","|_|_:###|____:---------------------------------------------------:____|###:_|_|","|_|_:###|_____________________________________________________________|###:_|_|"]

def leituraTeclado():
    global char, personagem_x, personagem_y, boneco, cenario_luta
    time.sleep(0.01)
    while 1:
        char = msvcrt.getch()
        
def comandosMovimento():
    global char, personagem_x, personagem_y, boneco, cenario_luta
    time.sleep(0.02)
    while 1:
        if str(char)=='a':
            personagem_x -=1
            char=0
        if str(char)=='d':
            personagem_x +=1
            char=0
        if str(char)=='w':
            personagem_y -=1
            char=0
        if str(char)=='s':
            personagem_y +=1
            char=0


def comandosGolpe():
    global char, personagem_x, personagem_y, boneco, cenario_luta
    time.sleep(0.03)
    while 1:
        if str(char)=='j':
            time.sleep(0.00001)
            if str(char)!='j':
                boneco=["  O"," /|V"," `|","  |\ "," /  |"]
                time.sleep(0.4)
                boneco=["  O__"," <|","  |","  |\ "," /  |"]
                time.sleep(0.3)
                boneco=["  O"," <|\ ","  |"," / \ ","|   |"]
                char=0

def cenarioPrintado():
    global char, personagem_x, personagem_y, boneco, cenario_luta
    while 1:
        cenario_total=cenario_luta
        n=0
        while n<len(boneco):
            j=0
            while j<len(boneco[n]):
                cenario_total[n+personagem_y][j+personagem_x]=boneco[n][j]
                j+=1
            n+=1
        os.system('cls')
        n=0
        while n<len(cenario_total):
            print ('\n'+str(cenario_total[n]))
            n+=1


try:
    thread.start_new_thread(leituraTeclado,())
    thread.start_new_thread(comandosMovimento,())
    thread.start_new_thread(comandosGolpe,())
    thread.start_new_thread(cenarioPrintado,())
except:
    print ("Erro: nao foi possivel iniciar o thread.")

while 1:
    pass
