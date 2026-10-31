# Browser copy of ../../absurdo.py: Python 3 syntax (2to3, thread -> _thread),
# and fixes two variables the threads used without "global" (intercala, da_vida). The rest is untouched.
from __future__ import print_function
import msvcrt, os, time, _thread, threading, random
while 1:
    char=0
    boneco=[[' ',' ','O'],[' ','<','|','\\',' '],[' ',' ','|'],[' ','/',' ','\\',' '],['|',' ',' ',' ','|']]
    umtreco=[[' ',' ','O'],[' ','/','|','>'],[' ',' ','|'],[' ','/',' ','\\'],['|',' ',' ',' ','|']]
    posicao_y=11
    posicao_x=24
    alvo_y=10
    alvo_x=50
    vida_personagem=300
    vida_alvo=300
    vida_total_alvo=vida_alvo
    vida_total_personagem=vida_personagem
    sentido=True
    da_vida=False
    ataque_personagem=8001
    defesa_personagem=8002
    ataque_alvo=6
    detectar=[False,False]
    defesa_alvo=5
    intercala=5
    #numpy
    inimigo_movimento=[False,False,False,False,False,False,False,False]
    #                   [0]A  [1]D [2]W  [3]S   [4]H  [5]J  [6]K  [7]L

    def maiorQueumINT(numero):
        if numero<1: numero=1
        else: numero=int(numero)
        return numero

    def leituraTeclado():
        global char
        time.sleep(0.01)
        while vida_personagem>0 and vida_alvo>0:
            char = msvcrt.getch()

    def condicoesAtaque():
        global inimigo_movimento, vida_alvo, alvo_y, posicao_y, alvo_x, posicao_x, vida_total_alvo, ataque_alvo, defesa_alvo, ataque_personagem, defesa_personagem, detectar, intercala
        if defesa_alvo>ataque_alvo:
            sorte=random.randrange(100)
            if defesa_alvo<ataque_personagem:
                if sorte<30: inimigo_movimento[4]=True
                elif sorte<55: inimigo_movimento[5]=True
                elif sorte<70: inimigo_movimento[6]=True
                elif sorte<100: inimigo_movimento[7]=True
            else:
                if sorte<30: inimigo_movimento[4]=True
                elif sorte<60: inimigo_movimento[5]=True
                elif sorte<80: inimigo_movimento[6]=True
                elif sorte<100: inimigo_movimento[7]=True
        elif ataque_alvo>defesa_alvo:
            sorte=random.randrange(100)
            if ataque_alvo<defesa_personagem:
                if sorte<15: inimigo_movimento[4]=True
                elif sorte<45: inimigo_movimento[5]=True
                elif sorte<70: inimigo_movimento[6]=True
                elif sorte<100: inimigo_movimento[7]=True
            else:
                if sorte<20: inimigo_movimento[4]=True
                elif sorte<40: inimigo_movimento[5]=True
                elif sorte<70: inimigo_movimento[6]=True
                elif sorte<100: inimigo_movimento[7]=True
        else:
            sorte=random.randrange(4)
            while intercala==sorte: sorte=random.randrange(4)
            if sorte==0: inimigo_movimento[4]=True
            elif sorte==1: inimigo_movimento[5]=True
            elif sorte==2: inimigo_movimento[6]=True
            elif sorte==3: inimigo_movimento[7]=True
            intercala=sorte

    def inteligenciaInimigo():
        global inimigo_movimento, vida_alvo, alvo_y, posicao_y, alvo_x, posicao_x, vida_total_alvo, ataque_alvo, defesa_alvo, ataque_personagem, defesa_personagem, detectar
        time.sleep(0.05)
        estrategia=[False, False]
        intercala=5
        while vida_personagem>0 and vida_alvo>0:
            time.sleep(0.08)
            inimigo_movimento=[False,False,False,False,False,False,False,False]
            sorte=random.randrange(100)
            if vida_alvo<vida_total_alvo*0.80 and detectar[1]==True and sorte<10:
                if vida_alvo<vida_total_alvo*0.10: sorte2=random.randrange(20)
                elif vida_alvo<vida_total_alvo*0.20: sorte2=random.randrange(15)
                elif vida_alvo<vida_total_alvo*0.40: sorte2=random.randrange(10)
                else: sorte2=random.randrange(5)
                if sorte2==1:
                    if alvo_y==10: inimigo_movimento[2]=True
                    else: inimigo_movimento[3]=True
            elif vida_alvo<vida_total_alvo*0.75 and detectar[0]==True and sorte<10:
                if vida_alvo<vida_total_alvo*0.05: sorte2=random.randrange(20)
                elif vida_alvo<vida_total_alvo*0.15: sorte2=random.randrange(15)
                elif vida_alvo<vida_total_alvo*0.35: sorte2=random.randrange(10)
                else: sorte2=random.randrange(5)
                if sorte2==1:
                    if alvo_y==10: inimigo_movimento[2]=True
                    else: inimigo_movimento[3]=True
            elif vida_alvo<vida_total_alvo*0.10 and alvo_x>posicao_x+8 or vida_alvo<vida_total_alvo*0.20 and alvo_x<posicao_x-8:
                if alvo_x<posicao_x+7: condicoesAtaque()
                elif alvo_x>posicao_x: inimigo_movimento[0]=True
                else: inimigo_movimento[1]=True
            elif vida_alvo<vida_total_alvo*0.20:
                if alvo_x<posicao_x+7: condicoesAtaque()
                elif alvo_x>posicao_x: inimigo_movimento[1]=True
                else: inimigo_movimento[0]=True
            elif estrategia[0]==True or alvo_x==posicao_x+5 and posicao_y!=alvo_y or alvo_x==posicao_x-5 and posicao_y!=alvo_y:
                if estrategia[1]==True:
                    if alvo_x>posicao_x+5:
                        inimigo_movimento[0]=True
                    elif alvo_x<posicao_x-5:
                        inimigo_movimento[1]=True
                    else:
                        inimigo_movimento[4]=True
                        estrategia[1]=False
                        estrategia[0]=False
                elif alvo_x==posicao_x+5 and alvo_x<65 or alvo_x==posicao_x+6 and alvo_x<65: 
                    inimigo_movimento[1]=True
                    estrategia[0]=True
                elif alvo_x==posicao_x-5 and alvo_x>9 or alvo_x==posicao_x-6:
                    inimigo_movimento[0]=True
                    estrategia[0]=True
                elif alvo_y>posicao_y: inimigo_movimento[3]=True
                elif alvo_y<posicao_y: inimigo_movimento[2]=True
                else: estrategia[1]=True
            elif sorte<60 and alvo_x>posicao_x+5 or sorte<60 and alvo_x<posicao_x-5:
                if alvo_x>posicao_x: inimigo_movimento[0]=True
                else: inimigo_movimento[1]=True
            elif sorte >70 and alvo_x>posicao_x+5 or sorte>70 and alvo_x<posicao_x-5:
                if alvo_x>posicao_x: inimigo_movimento[1]=True
                else: inimigo_movimento[0]=True
            elif posicao_y!=alvo_y:
                sorte=random.randrange(2)
                if alvo_y<posicao_y or sorte==1:
                    inimigo_movimento[2]=True
                else:
                    inimigo_movimento[3]=True
            else: condicoesAtaque()
                

    def movimentoInimigo():
        global umtreco, alvo_y, alvo_x, inimigo_movimento, vida_personagem, ataque_alvo, defesa_alvo, ataque_personagem, defesa_personagem, da_vida
        time.sleep(0.06)
        while vida_personagem>0 and vida_alvo>0:
            if(inimigo_movimento[3]==True and alvo_y>10):
                if (posicao_x!=alvo_x+4 and posicao_x!=alvo_x+3 and posicao_x!=alvo_x+2 and posicao_x!=alvo_x+1 and posicao_x!=alvo_x and posicao_x!=alvo_x-4 and posicao_x!=alvo_x-3 and posicao_x!=alvo_x-2 and posicao_x!=alvo_x-1):
                    alvo_y -=1
                elif (posicao_y==alvo_y-1 or posicao_y==alvo_y+2):
                    alvo_y -=1
                time.sleep(ataque_alvo*0.02)
            elif(inimigo_movimento[2]==True and alvo_y<12):
                if (posicao_x!=alvo_x+4 and posicao_x!=alvo_x+3 and posicao_x!=alvo_x+2 and posicao_x!=alvo_x+1 and posicao_x!=alvo_x and posicao_x!=alvo_x-4 and posicao_x!=alvo_x-3 and posicao_x!=alvo_x-2 and posicao_x!=alvo_x-1):
                    alvo_y +=1
                elif (posicao_y==alvo_y+1 or posicao_y==alvo_y-2):
                    alvo_y +=1
                time.sleep(ataque_alvo*0.02)
            elif(inimigo_movimento[0]==True and alvo_x>9):
                if (posicao_y!=alvo_y or posicao_y==alvo_y and posicao_x!=alvo_x+5):
                    alvo_x -=1
                time.sleep(ataque_alvo*0.02)
            elif(inimigo_movimento[1]==True and alvo_x<65):
                if (posicao_y!=alvo_y or posicao_y==alvo_y and posicao_x!=alvo_x-5):
                    alvo_x +=1
                time.sleep(ataque_alvo*0.02)
            elif(inimigo_movimento[4]==True):
                defesa_alvo=defesa_alvo*6
                if da_vida==False:
                    umtreco=[[' ',' ','O'],[' ',' ','|','V'],[' ',' ','|','/'],[' ',' ','|','\\'],[' ','/',' ',' ','|']]
                    time.sleep(0.05)
                    umtreco=[[' ',' ','O','|'],[' ',' ','|','-','-'],[' ',' ','|'],[' ',' ','|','\\'],[' ','/',' ',' ','|']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_personagem-=maiorQueumINT(0.3*ataque_alvo-(defesa_personagem))
                    time.sleep(0.09)
                    umtreco=[[' ',' ','O','.','|'],[' ',' ','|','/'],[' ',' ','|'],[' ',' ','|','\\'],[' ','/',' ',' ','|']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_personagem-=maiorQueumINT(0.3*ataque_alvo-(defesa_personagem))
                    time.sleep(0.09)
                    umtreco=[[' ',' ','O'],[' ','<','|','\\',' '],[' ',' ','|'],[' ','/',' ','\\',' '],['|',' ',' ',' ','|']]
                else:
                    umtreco=[[' ',' ','O'],[' ','V','|','\\',],[' ',' ','|','`'],[' ','/','|'],['|',' ',' ','\\']]
                    time.sleep(0.05)
                    umtreco=[[' ','|','O'],['-','-','|',' '],[' ',' ','|'],[' ','/','|'],['|',' ',' ','\\']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_personagem-=maiorQueumINT(0.3*ataque_alvo-(defesa_personagem))
                    time.sleep(0.09)
                    umtreco=[['|','.','O'],[' ','\\','|'],[' ',' ','|'],[' ','/','|'],['|',' ',' ','\\']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_personagem-=maiorQueumINT(0.3*ataque_alvo-(defesa_personagem))
                    time.sleep(0.09)
                    umtreco=[[' ',' ','O'],[' ','/','|','>'],[' ',' ','|'],[' ','/',' ','\\'],['|',' ',' ',' ','|']]
                defesa_alvo=int(defesa_alvo/6)
            elif(inimigo_movimento[5]==True):
                defesa_alvo=defesa_alvo*4
                if da_vida==False:
                    umtreco=[[' ',' ','O'],[' ','/','|','V'],[' ','`','|'],[' ',' ','|','\\'],[' ','/',' ',' ','|']]
                    time.sleep(0.05)
                    umtreco=[[' ',' ','O','_','_'],[' ','<','|','-','-'],[' ',' ','|'],[' ',' ','|','\\'],[' ','/',' ',' ','|']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_personagem-=0.5*ataque_alvo-(defesa_personagem)
                    time.sleep(0.09)
                    umtreco=[[' ',' ','O'],[' ','`','|','=','='],[' ',' ','|'],[' ',' ','|','\\'],[' ','/',' ',' ','|']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_personagem-=0.5*ataque_alvo-(defesa_personagem)
                    time.sleep(0.09)
                    umtreco=[[' ',' ','O'],[' ','<','|','\\',' '],[' ',' ','|'],[' ','/',' ','\\',' '],['|',' ',' ',' ','|']]
                else:
                    umtreco=[[' ',' ','O'],[' ','V','|','\\',],[' ',' ','|','`'],[' ','/','|'],['|',' ',' ','\\']]
                    time.sleep(0.05)
                    umtreco=[['_','_','O'],['-','-','|','>'],[' ',' ','|'],[' ','/','|'],['|',' ',' ','\\']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_personagem-=maiorQueumINT(0.5*ataque_alvo-(defesa_personagem))
                    time.sleep(0.09)
                    umtreco=[[' ',' ','O'],['=','=','|','`'],[' ',' ','|'],[' ','/','|'],['|',' ',' ','\\']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_personagem-=maiorQueumINT(0.5*ataque_alvo-(defesa_personagem))
                    time.sleep(0.09)
                    umtreco=[[' ',' ','O'],[' ','/','|','>'],[' ',' ','|'],[' ','/',' ','\\'],['|',' ',' ',' ','|']]
                defesa_alvo=int(defesa_alvo/4)
            elif(inimigo_movimento[6]==True):
                defesa_alvo=int(defesa_alvo/6)
                if da_vida==False:
                    umtreco=[[' ',' ','O'],[' ','<','|','\\'],[' ',' ','|','_'],[' ',' ','|',' ','/'],[' ','/',' ']]
                    time.sleep(0.05)
                    umtreco=[[' ',' ','O'],[' ','<','|','-',' ','/'],[' ',' ','|','/'],[' ',' ','|'],[' ','/',' ']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_personagem-=maiorQueumINT(2.5*ataque_alvo-(defesa_personagem))
                    time.sleep(0.18)
                    umtreco=[[' ',' ','O'],[' ','<','|','\\',' '],[' ',' ','|'],[' ','/',' ','\\',' '],['|',' ',' ',' ','|']]
                else:
                    umtreco=[[' ',' ',' ','O'],[' ',' ','/','|','>'],[' ',' ','_','|'],[' ','\\',' ','|'],[' ',' ',' ',' ','\\']]
                    time.sleep(0.05)
                    umtreco=[[' ',' ',' ','O'],['\\',' ','-','|','>'],[' ',' ','\\','|'],[' ',' ',' ','|'],[' ',' ',' ',' ','\\']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_personagem-=maiorQueumINT(2.5*ataque_alvo-(defesa_personagem))
                    time.sleep(0.18)
                    umtreco=[[' ',' ','O'],[' ','/','|','>'],[' ',' ','|'],[' ','/',' ','\\'],['|',' ',' ',' ','|']]
                defesa_alvo=defesa_alvo*6
            elif(inimigo_movimento[7]==True):
                defesa_alvo=int(defesa_alvo/4)
                if da_vida==False:
                    umtreco=[[' ',' ','O'],[' ','/','|','V'],[' ',' ','|','_'],[' ','/',' ',' ','|'],['|']]
                    time.sleep(0.05)
                    umtreco=[['O','_','|'],['<','\\'],[' ',' ','\\','_','_','_','_'],[' ','/'],['|']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_personagem-=maiorQueumINT(1.5*ataque_alvo-(defesa_personagem))
                    time.sleep(0.18)
                    umtreco=[[' ',' ','O'],[' ','<','|','\\',' '],[' ',' ','|'],[' ','/',' ','\\',' '],['|',' ',' ',' ','|']]
                else:
                    umtreco=[[' ',' ',' ','O'],[' ',' ','V','|','\\'],[' ',' ','_','|'],[' ','|',' ',' ','\\'],[' ',' ',' ',' ',' ','|']]
                    time.sleep(0.05)
                    umtreco=[[' ',' ',' ',' ','|','_','O'],[' ',' ',' ',' ',' ','/','>'],['_','_','_','_','/'],[' ',' ',' ',' ','\\'],[' ',' ',' ',' ',' ','|']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_personagem-=maiorQueumINT(1.5*ataque_alvo-(defesa_personagem))
                    time.sleep(0.18)
                    umtreco=[[' ',' ','O'],[' ','/','|','>'],[' ',' ','|'],[' ','/',' ','\\'],['|',' ',' ',' ','|']]
                defesa_alvo=defesa_alvo*4
            if(inimigo_movimento[0]==True or inimigo_movimento[1]==True):
                if alvo_x<posicao_x:
                    umtreco=[[' ',' ','O'],[' ','/','|','\\','.'],[' ','`','|'],['_','/',' ','\\'],[' ',' ',' ',' ','|']]
                    time.sleep(0.02)
                    umtreco=[[' ',' ','O'],[' ','<','|','V'],[' ',' ','|','_'],[' ',' ','|',' ','|'],[' ','/']]
                    time.sleep(0.02)
                    umtreco=[[' ',' ','O'],[' ','<','|','\\',' '],[' ',' ','|'],[' ','/',' ','\\',' '],['|',' ',' ',' ','|']]
                    da_vida=False
                else:
                    umtreco=[[' ',' ','O'],['.','/','|','\\'],[' ',' ','|','`'],[' ','/',' ','\\','_'],['|']]
                    time.sleep(0.02)
                    umtreco=[[' ',' ','O'],[' ','V','|','>'],[' ','_','|'],['|',' ','|'],[' ',' ',' ','\\']]
                    time.sleep(0.02)
                    umtreco=[[' ',' ','O'],[' ','/','|','>'],[' ',' ','|'],[' ','/',' ','\\'],['|',' ',' ',' ','|']]
                    da_vida=True

    def comandosMovimento():
        global char, posicao_x, posicao_y, boneco, alvo_y
        time.sleep(0.04)
        while vida_personagem>0 and vida_alvo>0:
            time.sleep(ataque_personagem*0.02)
            if str(char)=='a':
                if(posicao_x>9):
                    if (posicao_y!=alvo_y or posicao_y==alvo_y and posicao_x!=alvo_x+5):
                        posicao_x -=1
                time.sleep(0.04)
                char=0
            if str(char)=='d':
                if(posicao_x<65):
                    if (posicao_y!=alvo_y or posicao_y==alvo_y and posicao_x!=alvo_x-5):
                        posicao_x +=1
                time.sleep(0.04)
                char=0
            if str(char)=='w':
                if(posicao_y>10):
                    if (posicao_x!=alvo_x+4 and posicao_x!=alvo_x+3 and posicao_x!=alvo_x+2 and posicao_x!=alvo_x+1 and posicao_x!=alvo_x and posicao_x!=alvo_x-4 and posicao_x!=alvo_x-3 and posicao_x!=alvo_x-2 and posicao_x!=alvo_x-1):
                        posicao_y -=1
                    elif (posicao_y==alvo_y-1 or posicao_y==alvo_y+2):
                        posicao_y -=1
                char=0
            if str(char)=='s':
                if(posicao_y<12):
                    if (posicao_x!=alvo_x+4 and posicao_x!=alvo_x+3 and posicao_x!=alvo_x+2 and posicao_x!=alvo_x+1 and posicao_x!=alvo_x and posicao_x!=alvo_x-4 and posicao_x!=alvo_x-3 and posicao_x!=alvo_x-2 and posicao_x!=alvo_x-1):
                        posicao_y +=1
                    elif (posicao_y==alvo_y+1 or posicao_y==alvo_y-2):
                        posicao_y +=1
                char=0

    def animacaoMovimento():
        global char, boneco, posicao_x, posicao_y, sentido, alvo_x, alvo_y
        time.sleep(0.05)
        while vida_personagem>0 and vida_alvo>0:
            if str(char)=='a' and posicao_x>9 or str(char)=='d' and posicao_x<65:
                if alvo_x>posicao_x:
                    boneco=[[' ',' ','O'],[' ','/','|','\\','.'],[' ','`','|'],['_','/',' ','\\'],[' ',' ',' ',' ','|']]
                    time.sleep(0.02)
                    boneco=[[' ',' ','O'],[' ','<','|','V'],[' ',' ','|','_'],[' ',' ','|',' ','|'],[' ','/']]
                    time.sleep(0.02)
                    boneco=[[' ',' ','O'],[' ','<','|','\\',' '],[' ',' ','|'],[' ','/',' ','\\',' '],['|',' ',' ',' ','|']]
                    sentido=True
                else:
                    boneco=[[' ',' ','O'],['.','/','|','\\'],[' ',' ','|','`'],[' ','/',' ','\\','_'],['|']]
                    time.sleep(0.02)
                    boneco=[[' ',' ','O'],[' ','V','|','>'],[' ','_','|'],['|',' ','|'],[' ',' ',' ','\\']]
                    time.sleep(0.02)
                    boneco=[[' ',' ','O'],[' ','/','|','>'],[' ',' ','|'],[' ','/',' ','\\'],['|',' ',' ',' ','|']]
                    sentido=False

    def golpesAnimacao():
        global char, boneco, posicao_x, posicao_y, sentido, vida_alvo, alvo_x, alvo_y, ataque_alvo, defesa_alvo, ataque_personagem, defesa_personagem, detectar
        time.sleep(0.06)
        ja_deu_cotovelo=False
        ja_deu_soco=False
        ja_deu_chute=False
        ja_deu_bica=False
        while vida_personagem>0 and vida_alvo>0:
            detectar=[False,False]
            if str(char)=='h' and ja_deu_cotovelo==False:
                defesa_personagem=defesa_personagem*6
                if sentido==True:
                    boneco=[[' ',' ','O'],[' ',' ','|','V'],[' ',' ','|','/'],[' ',' ','|','\\'],[' ','/',' ',' ','|']]
                    detectar[0]=True
                    time.sleep(0.05)
                    boneco=[[' ',' ','O','|'],[' ',' ','|','-','-'],[' ',' ','|'],[' ',' ','|','\\'],[' ','/',' ',' ','|']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_alvo-=maiorQueumINT(0.3*ataque_personagem-(defesa_alvo))
                    detectar[1]=True
                    time.sleep(0.09)
                    boneco=[[' ',' ','O','.','|'],[' ',' ','|','/'],[' ',' ','|'],[' ',' ','|','\\'],[' ','/',' ',' ','|']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_alvo-=maiorQueumINT(0.3*ataque_personagem-(defesa_alvo))
                    time.sleep(0.09)
                    boneco=[[' ',' ','O'],[' ','<','|','\\',' '],[' ',' ','|'],[' ','/',' ','\\',' '],['|',' ',' ',' ','|']]
                else:
                    boneco=[[' ',' ','O'],[' ','V','|','\\',],[' ',' ','|','`'],[' ','/','|'],['|',' ',' ','\\']]
                    detectar[0]=True
                    time.sleep(0.05)
                    boneco=[[' ','|','O'],['-','-','|',' '],[' ',' ','|'],[' ','/','|'],['|',' ',' ','\\']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_alvo-=maiorQueumINT(0.3*ataque_personagem-(defesa_alvo))
                    detectar[1]=True
                    time.sleep(0.09)
                    boneco=[['|','.','O'],[' ','\\','|'],[' ',' ','|'],[' ','/','|'],['|',' ',' ','\\']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_alvo-=maiorQueumINT(0.3*ataque_personagem-(defesa_alvo))
                    time.sleep(0.09)
                    boneco=[[' ',' ','O'],[' ','/','|','>'],[' ',' ','|'],[' ','/',' ','\\'],['|',' ',' ',' ','|']]
                time.sleep(ataque_personagem*0.02)
                defesa_personagem=int(defesa_personagem/6)
                ja_deu_cotovelo=True
                ja_deu_soco=False
                ja_deu_chute=False
                ja_deu_bica=False
            if str(char)=='j' and ja_deu_soco==False:
                defesa_personagem=defesa_personagem*4
                if sentido==True:
                    boneco=[[' ',' ','O'],[' ','/','|','V'],[' ','`','|'],[' ',' ','|','\\'],[' ','/',' ',' ','|']]
                    detectar[0]=True
                    time.sleep(0.05)
                    boneco=[[' ',' ','O','_','_'],[' ','<','|','-','-'],[' ',' ','|'],[' ',' ','|','\\'],[' ','/',' ',' ','|']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_alvo-=maiorQueumINT(0.5*ataque_personagem-(defesa_alvo))
                    detectar[1]=True
                    time.sleep(0.09)
                    boneco=[[' ',' ','O'],[' ','`','|','=','='],[' ',' ','|'],[' ',' ','|','\\'],[' ','/',' ',' ','|']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_alvo-=maiorQueumINT(0.5*ataque_personagem-(defesa_alvo))
                    time.sleep(0.09)
                    boneco=[[' ',' ','O'],[' ','<','|','\\',' '],[' ',' ','|'],[' ','/',' ','\\',' '],['|',' ',' ',' ','|']]
                else:
                    boneco=[[' ',' ','O'],[' ','V','|','\\',],[' ',' ','|','`'],[' ','/','|'],['|',' ',' ','\\']]
                    detectar[0]=True
                    time.sleep(0.05)
                    boneco=[['_','_','O'],['-','-','|','>'],[' ',' ','|'],[' ','/','|'],['|',' ',' ','\\']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_alvo-=maiorQueumINT(0.5*ataque_personagem-(defesa_alvo))
                    detectar[1]=True
                    time.sleep(0.09)
                    boneco=[[' ',' ','O'],['=','=','|','`'],[' ',' ','|'],[' ','/','|'],['|',' ',' ','\\']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_alvo-=maiorQueumINT(0.5*ataque_personagem-(defesa_alvo))
                    time.sleep(0.09)
                    boneco=[[' ',' ','O'],[' ','/','|','>'],[' ',' ','|'],[' ','/',' ','\\'],['|',' ',' ',' ','|']]
                time.sleep(ataque_personagem*0.02)
                defesa_personagem=int(defesa_personagem/4)
                ja_deu_cotovelo=False
                ja_deu_soco=True
                ja_deu_chute=False
                ja_deu_bica=False
            if str(char)=='l' and ja_deu_chute==False:
                defesa_personagem=int(defesa_personagem/6)
                if sentido==True:
                    boneco=[[' ',' ','O'],[' ','<','|','\\'],[' ',' ','|','_'],[' ',' ','|',' ','/'],[' ','/',' ']]
                    detectar[1]=True
                    time.sleep(0.05)
                    boneco=[[' ',' ','O'],[' ','<','|','-',' ','/'],[' ',' ','|','/'],[' ',' ','|'],[' ','/',' ']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_alvo-=maiorQueumINT(2.5*ataque_personagem-(defesa_alvo))
                    time.sleep(0.18)
                    boneco=[[' ',' ','O'],[' ','<','|','\\',' '],[' ',' ','|'],[' ','/',' ','\\',' '],['|',' ',' ',' ','|']]
                else:
                    boneco=[[' ',' ',' ','O'],[' ',' ','/','|','>'],[' ',' ','_','|'],[' ','\\',' ','|'],[' ',' ',' ',' ','\\']]
                    detectar[1]=True
                    time.sleep(0.05)
                    boneco=[[' ',' ',' ','O'],['\\',' ','-','|','>'],[' ',' ','\\','|'],[' ',' ',' ','|'],[' ',' ',' ',' ','\\']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_alvo-=maiorQueumINT(2.5*ataque_personagem-(defesa_alvo))
                    time.sleep(0.18)
                    boneco=[[' ',' ','O'],[' ','/','|','>'],[' ',' ','|'],[' ','/',' ','\\'],['|',' ',' ',' ','|']]
                time.sleep(ataque_personagem*0.02)
                defesa_personagem=defesa_personagem*6
                ja_deu_cotovelo=False
                ja_deu_chute=True
                ja_deu_soco=False
                ja_deu_bica=False
            if str(char)=='k' and ja_deu_bica==False:
                defesa_personagem=int(defesa_personagem/4)
                if sentido==True:
                    boneco=[[' ',' ','O'],[' ','/','|','V'],[' ',' ','|','_'],[' ','/',' ',' ','|'],['|']]
                    detectar[1]=True
                    time.sleep(0.05)
                    boneco=[['O','_','|'],['<','\\'],[' ',' ','\\','_','_','_','_'],[' ','/'],['|']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_alvo-=maiorQueumINT(1.5*ataque_personagem-(defesa_alvo))
                    time.sleep(0.18)
                    boneco=[[' ',' ','O'],[' ','<','|','\\',' '],[' ',' ','|'],[' ','/',' ','\\',' '],['|',' ',' ',' ','|']]
                else:
                    boneco=[[' ',' ',' ','O'],[' ',' ','V','|','\\'],[' ',' ','_','|'],[' ','|',' ',' ','\\'],[' ',' ',' ',' ',' ','|']]
                    detectar[1]=True
                    time.sleep(0.05)
                    boneco=[[' ',' ',' ',' ','|','_','O'],[' ',' ',' ',' ',' ','/','>'],['_','_','_','_','/'],[' ',' ',' ',' ','\\'],[' ',' ',' ',' ',' ','|']]
                    if alvo_x==posicao_x+5 and alvo_y==posicao_y or alvo_x==posicao_x-5 and alvo_y==posicao_y: vida_alvo-=maiorQueumINT(1.5*ataque_personagem-(defesa_alvo))
                    time.sleep(0.18)
                    boneco=[[' ',' ','O'],[' ','/','|','>'],[' ',' ','|'],[' ','/',' ','\\'],['|',' ',' ',' ','|']]
                time.sleep(ataque_personagem*0.02)
                defesa_personagem=defesa_personagem*4
                ja_deu_cotovelo=False
                ja_deu_bica=True
                ja_deu_soco=False
                ja_deu_chute=False

    def cenarioPrintado():
        global char, posicao_x, posicao_y, boneco, umtreco, alvo_x, alvo_y,vida_personagem, vida_alvo, vida_total_personagem, vida_total_alvo
        time.sleep(0.07)
        while vida_personagem>0 and vida_alvo>0:
            time.sleep(1/30)
            buneco=boneco
            traveco=umtreco
            cenario_texto=''
            cenario_muda=[['_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_'],
                          ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
                          ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',' ',' ','|',' ',' ','|',' ',' ','|',' ',' ','|',' ',' ','|',' ',' ','|',' ',' ','|',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
                          ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','_','_','|','_','_','|','_','_','|','_','_','|','_','_','|','_','_','|','_','_','|','_','_','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
                          ['|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',' ',' ','|',' ',' ','|',' ',' ','|',' ',' ','|',' ',' ','|',' ',' ','|',' ',' ','|',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|'],
                          ['|',' ',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','_','_','|','_','_','|','_','_','|','_','_','|','_','_','|','_','_','|','_','_','|','_','_','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',' ',' ',' ',' ',' ',' ',' ',' ','|'],
                          ['|',' ',' ',' ',' ',' ',' ',' ','/','|','_',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','_','|','\\',' ',' ',' ',' ',' ',' ',' ','|'],
                          ['|',' ',' ',' ',' ',' ','/',' ',' ','|','#',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','#','|',' ',' ','\\',' ',' ',' ',' ',' ','|'],
                          ['|',' ',' ',' ','/',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','\\',' ',' ',' ','|'],
                          ['|',' ','/',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','_','|','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','|','_',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','\\',' ','|'],
                          ['|',' ','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|',' ','|'],
                          ['|',' ','|',' ',' ',' ',';','`','|',' ',' ',' ',' ',' ',' ',' ',' ','_','|','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','|','_',' ',' ',' ',' ',' ',' ',' ',' ','|','`',':',' ',' ',' ','|',' ','|'],
                          ['|',' ','|',' ',' ',';','.','#','|',' ',' ',' ',' ',' ',' ',' ','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-',' ',' ',' ',' ',' ',' ',' ','|','#','`',':',' ',' ','|',' ','|'],
                          ['|',' ','|',' ',':','.','#','#','|',' ',' ',' ',' ',' ','_','|','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','|','_',' ',' ',' ',' ',' ','|','#','#','`',':',' ','|',' ','|'],
                          ['|','_','|','_',':','#','#','#','|','_','_','_','_',':','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-','-',':','_','_','_','_','|','#','#','#',':','_','|','_','|'],
                          ['|','_','|','_',':','#','#','#','|',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ','|','#','#','#',':','_','|','_','|'],
                          ['|','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','_','|']]
            n=0
            while n<len(traveco):
                j=0
                while j<len(traveco[n]):
                    if traveco[n][j]!=' ': cenario_muda[alvo_y+n][alvo_x+j]=traveco[n][j]
                    j+=1
                n+=1
            n=0
            while n<len(buneco):
                j=0
                while j<len(buneco[n]):
                    if buneco[n][j]!=' ': cenario_muda[posicao_y+n][posicao_x+j]=buneco[n][j]
                    j+=1
                n+=1
            n=0
            while n<len(cenario_muda):
                j=0
                while j<len(cenario_muda[n]):
                    cenario_texto+=cenario_muda[n][j]
                    j+=1
                cenario_texto+='\n'
                n+=1
            if vida_personagem<0: vida_personagem=0
            if vida_alvo<0: vida_alvo=0
            barra_personagem="["+"|"*int(vida_personagem*30/vida_total_personagem)+"-"*int(30-(vida_personagem*30/vida_total_personagem))+"]"
            barra_alvo="["+"-"*int(30-(vida_alvo*30/vida_total_alvo))+"|"*int(vida_alvo*30/vida_total_alvo)+"]"
            os.system('cls')
            print('_'*79+'\n'+' P1:'+str(barra_personagem)+' '*7+str(barra_alvo)+':P2\n'+cenario_texto+'\n\tUse W A S D para mover\t\tPara atacar alterne H J K L\n'+str(alvo_x)+str(posicao_x))

    os.system('cls')
    os.system('color 70')
    while ataque_personagem>10:
        print ('\nComandos:\n H : Cotovelada \t 0.6 ATK  3.00 DEF\n J : Socos Alternados \t 1.0 ATK  2.00 DEF\n K : Chute baixo \t 1.5 ATK  0.50 DEF\n L : Chute alto \t 2.5 ATK  0.25 DEF\n\nVoce tem direito a APENAS 10 pontos entre ataque E defesa.\nSua velocidade sera definida inversamente ao seu ataque.\nMe diga o quanto que quer em ataque, colocarei o resto em defesa:')
        ataque_personagem=eval(input('\n-'))
        ataque_personagem=int(ataque_personagem)
        os.system('cls')
    defesa_personagem=15-ataque_personagem
    ataque_personagem+=1
    ataque_alvo=random.randrange(11)+1
    defesa_alvo=15-ataque_alvo

    try:
        _thread.start_new_thread(leituraTeclado,())
        _thread.start_new_thread(comandosMovimento,())
        _thread.start_new_thread(animacaoMovimento,())
        _thread.start_new_thread(inteligenciaInimigo,())
        _thread.start_new_thread(movimentoInimigo,())
        _thread.start_new_thread(golpesAnimacao,())
        _thread.start_new_thread(cenarioPrintado,())
    except:
        print ("Erro: nao foi possivel iniciar o thread.")

    while vida_personagem>0 and vida_alvo>0:
        pass
    time.sleep(1)
    os.system('cls')
    time.sleep(1)
    if vida_alvo>0:
        os.system('color 4c')
        for n in range(50):
            print('VOCE PERDEU!'.rjust(45))
            time.sleep(n*0.01)
    else:
        os.system('color 9f')
        for n in range(100):
            print('VOCE VENCEU!'.rjust(45))
            time.sleep(0.01)
