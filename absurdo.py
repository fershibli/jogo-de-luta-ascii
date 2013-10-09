from __future__ import print_function
import msvcrt
import os
import time
import thread
import threading
char=0
personagem_x=1
personagem_y=1
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
        os.system('cls')
        contador=0
        i=0
        for n in cenario_luta:
            e=0
            f=0
            while e<len(cenario_luta[i]):
                if i-contador==personagem_y and e-f==personagem_x:
                    if boneco[0+contador][f]==' ':
                        print(cenario_luta[i][e],end='')
                    else:
                        print(boneco[0+contador][f],end='')
                    f+=1
                else:
                    print(cenario_luta[i][e],end='')
                e+=1
            if len(boneco)>contador and personagem_y==i-contador:
                contador+=1
            i+=1
            print('\n',end='')


try:
    thread.start_new_thread(leituraTeclado,())
    thread.start_new_thread(comandosMovimento,())
    thread.start_new_thread(comandosGolpe,())
    thread.start_new_thread(cenarioPrintado,())
except:
    print ("Erro: nao foi possivel iniciar o thread.")

while 1:
    pass
