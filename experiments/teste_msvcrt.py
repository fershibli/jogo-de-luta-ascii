import msvcrt
import os
import time
import thread
import threading
boneco="O"
personagem_x=20
personagem_y=20
char=0
def leituraTeclado():
    global char, personagem_x, personagem_y, boneco
    time.sleep(0.01)
    while 1:
        char = msvcrt.getch()
        
def comandosMovimento():
    global char, personagem_x, personagem_y, boneco
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
    global char, personagem_x, personagem_y, boneco
    time.sleep(0.03)
    while 1:
        if str(char)=='j':
            time.sleep(0.00001)
            if str(char)!='j':
                boneco='X'
                time.sleep(1)
                boneco='O'
                char=0

def cenarioPrintado():
    global char, personagem_x, personagem_y, boneco
    time.sleep(0.04)
    while 1:
        os.system('cls')
        print (str("\n"*personagem_y)+str(" "*personagem_x)+str(boneco))
        os.system('cls')
        print (str("\n"*personagem_y)+str(" "*(personagem_x+1))+str(boneco))

try:
    thread.start_new_thread(leituraTeclado,())
    thread.start_new_thread(comandosMovimento,())
    thread.start_new_thread(comandosGolpe,())
    thread.start_new_thread(cenarioPrintado,())
except:
    print "Erro: nao foi possivel iniciar o thread."

while 1:
    pass
