# -*- coding: cp1252 -*-
from __future__ import print_function
import msvcrt, os, time, thread, random, socket
socketServidora=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
socketServidora.bind(("", 20134))
socketClienta=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
IP_visivel=socket.gethostbyname(socket.gethostname())
data=''
trava=True
nome=raw_input('\nQual eh o seu nome?\n-').capitalize()
def recebeMensagem():
    global data, trava, utocubano
    while 1:
        if trava==True:
            data,addr=socketServidora.recvfrom(1024)
        else:
            utocubano,addr=socketServidora.recvfrom(1024)
            time.sleep(0.01)
            if utocubano!='0123456789IPRECEBIDOCOMSUCESSO' and utocubano!=IP_amigo: print(utocubano)

while 8001:
    print ('\n Seu IP: '+str(IP_visivel)+' (Feche outras conexoes, como o HAMACHI).')
    resposta=input('\nEscolha:\n\n 1 : Se conectar\n\n 2 : Esperar\n\n-')
    if resposta==1:
        posicao_inicial=1
        try:
            thread.start_new_thread(recebeMensagem,())
        except:
            print('\n\n\nERRO: Nao pode iniciar thread de recebimento de mensagens!\n\n\n')
        IP_amigo=raw_input('\nQual eh o IP do seu amigo?\n-')
        while data!='0123456789IPRECEBIDOCOMSUCESSO':
            socketClienta.sendto(IP_visivel,(IP_amigo,20134))
        
        break
    elif resposta==2:
        posicao_inicial=2
        data,addr=socketServidora.recvfrom(1024)
        IP_amigo=data
        socketClienta.sendto('0123456789IPRECEBIDOCOMSUCESSO',(IP_amigo,20134))
        try:
            thread.start_new_thread(recebeMensagem,())
        except:
            print('\n\n\nERRO: Nao pode iniciar thread de recebimento de mensagens!\n\n\n')

        break
    else:
        print('Digite 1 ou 2!')
print ('\n\n##################\n### CONECTADO! ###\n##### JOGUE! #####\n##################\n\n')
trava=False

while 1:
    if posicao_inicial==1:
        boneco=[[' ',' ','O'],[' ','<','|','\\',' '],[' ',' ','|'],[' ','/',' ','\\',' '],['|',' ',' ',' ','|']]
        umtreco=[[' ',' ','O'],[' ','/','|','>'],[' ',' ','|'],[' ','/',' ','\\'],['|',' ',' ',' ','|']]
        posicao_x=24
        alvo_x=50
        sentido=True
        da_vida=False
    else:
        boneco=[[' ',' ','O'],[' ','/','|','>'],[' ',' ','|'],[' ','/',' ','\\'],['|',' ',' ',' ','|']]
        umtreco=[[' ',' ','O'],[' ','<','|','\\',' '],[' ',' ','|'],[' ','/',' ','\\',' '],['|',' ',' ',' ','|']]
        posicao_x=50
        alvo_x=24
        sentido=False
        da_vida=True
    char=0
    utocubano=0
    posicao_y=10
    alvo_y=10
    vida_personagem=300
    vida_alvo=300
    vida_total_alvo=vida_alvo
    vida_total_personagem=vida_personagem
    ataque_personagem=8001
    defesa_personagem=8002
    ataque_alvo=6
    detectar=[False,False]
    defesa_alvo=5
    ##mel sz##
    #numpy
    #                   [0]A  [1]D [2]W  [3]S   [4]H  [5]J  [6]K  [7]L

    def maiorQueumINT(numero):
        if numero<1: numero=1
        else: numero=int(numero)
        return numero

    def leituraTeclado():
        global char, IP_amigo
        time.sleep(0.01)
        while vida_personagem>0 and vida_alvo>0:
            char = msvcrt.getch()
            socketClienta.sendto(char,(IP_amigo,20134))

    def movimentoInimigo():
        global umtreco, alvo_y, alvo_x, inimigo_movimento, vida_personagem, ataque_alvo, defesa_alvo, ataque_personagem, defesa_personagem,utocubano
        time.sleep(0.06)
        while vida_personagem>0 and vida_alvo>0:
            if(utocubano=='s' and alvo_y>10):
                if (posicao_x!=alvo_x+4 and posicao_x!=alvo_x+3 and posicao_x!=alvo_x+2 and posicao_x!=alvo_x+1 and posicao_x!=alvo_x and posicao_x!=alvo_x-4 and posicao_x!=alvo_x-3 and posicao_x!=alvo_x-2 and posicao_x!=alvo_x-1):
                    alvo_y -=1
                elif (posicao_y==alvo_y-1 or posicao_y==alvo_y+2):
                    alvo_y -=1
                time.sleep(ataque_alvo*0.02)
            elif(utocubano=='w' and alvo_y<12):
                if (posicao_x!=alvo_x+4 and posicao_x!=alvo_x+3 and posicao_x!=alvo_x+2 and posicao_x!=alvo_x+1 and posicao_x!=alvo_x and posicao_x!=alvo_x-4 and posicao_x!=alvo_x-3 and posicao_x!=alvo_x-2 and posicao_x!=alvo_x-1):
                    alvo_y +=1
                elif (posicao_y==alvo_y+1 or posicao_y==alvo_y-2):
                    alvo_y +=1
                time.sleep(ataque_alvo*0.02)
            elif(utocubano=='a' and alvo_x>9):
                if (posicao_y!=alvo_y or posicao_y==alvo_y and posicao_x!=alvo_x+5):
                    alvo_x -=1
                time.sleep(ataque_alvo*0.02)
            elif(utocubano=='d' and alvo_x<65):
                if (posicao_y!=alvo_y or posicao_y==alvo_y and posicao_x!=alvo_x-5):
                    alvo_x +=1
                time.sleep(ataque_alvo*0.02)
            elif(utocubano=='h'):
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
            elif(utocubano=='j'):
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
            elif(utocubano=='l'):
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
            elif(utocubano=='k'):
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
            if(utocubano=='a' or utocubano=='d'):
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
        global char, posicao_x, posicao_y, boneco, umtreco, alvo_x, alvo_y,vida_personagem, vida_alvo, vida_total_personagem, vida_total_alvo,nome
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
            frame='_'*79+'\n'+' P1:'+str(barra_personagem)+' '*7+str(barra_alvo)+':P2\n'+cenario_texto+'\n\tUse W A S D para mover\t\tPara atacar alterne H J K L\n'+str(alvo_x)+str(posicao_x)
            os.system('cls')
            print (frame)

    os.system('cls')
    os.system('color 70')
    ataque_personagem+=random.randrange(11)+1
    defesa_personagem=15-ataque_personagem
    ataque_alvo=random.randrange(11)+1
    defesa_alvo=15-ataque_alvo
    try:
        thread.start_new_thread(leituraTeclado,())
        thread.start_new_thread(comandosMovimento,())
        thread.start_new_thread(animacaoMovimento,())
        thread.start_new_thread(movimentoInimigo,())
        thread.start_new_thread(golpesAnimacao,())
        thread.start_new_thread(cenarioPrintado,())
    except:
        print ("Erro: nao foi possivel iniciar o thread.")

    while vida_personagem>0 and vida_alvo>0:
        pass
    time.sleep(1)
    os.system('cls')
    time.sleep(1)
    if vida_alvo>0:
        os.system('color 4c')
        for n in range(10):
            print('VOCE PERDEU!'.rjust(45))
            time.sleep(0.02)
    else:
        os.system('color 9f')
        for n in range(10):
            print('VOCE VENCEU!'.rjust(45))
            time.sleep(0.02)
verificaMsg.fecharVerificaMensagens()
