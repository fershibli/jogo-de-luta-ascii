#!/usr/bin/python:
import thread
import time

# Definindo uma funcao para o thread:
def print_time (nomedothread, delay):
    conta = 0
    while conta < 5:
        time.sleep(delay)
        conta += 1
        print "%s: %s" % (nomedothread, time.ctime(time.time()) )

# Criando o thread:
try:
    thread.start_new_thread( print_time, ("Thread-1", 2, ) )
    thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
    print "Erro: nao foi possivel iniciar o thread."

while 1:
    pass
