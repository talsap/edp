# -*- coding: utf-8 -*-

'''Bibliotecas'''

import time
import serial
import bancodedados
import numpy as np
from sys import *
from serial.tools import list_ports

'''Variaveis Globais'''
opcaoC = "C"    '''conectado'''
opcaoD = "D"    '''desconectado'''
opcaoI = "I"    '''DNIT134'''
opcaoE = "E"    '''CAMARA DE PRESSAO'''
opcaoM = "M"    '''MOTOR DE PASSOS'''
opcaoB = "B"    '''Break'''
opcaoG = "G"    '''Golpes'''
Y = []          #Array Deformações
T = []          #Array tempo grafico'''

'''Port Serial'''
portlist = [port for port,desc,hwin in list_ports.comports()]
conexao = serial.Serial()
conexao.baudrate = 250000

'''Coeficientes da calibracao'''
L = bancodedados.LVDT()
A1 = float(L[0])
B1 = float(L[1])
A2 = float(L[2])
B2 = float(L[3])

#-------------------------------------------------------------------
def connect():
    i = 0
    condicaoConeccao = False
    try:
        while i < len(portlist):
            conexao.port = portlist[i]
            try:
                conexao.open()
                if conexao.isOpen() == True:
                    print("Verificando Conexao com porta serial "+conexao.port+"...\n")
                    conexao.write(opcaoC)
                    conexao.timeout = 1
                    a = conexao.readline()
                    if a[0] == "c":
                        print a
                        condicaoConeccao = True
                        return conexao.port, "connectado"
                    else:
                        print "notconectado"
                        conexao.close()
            except:
                conexao.close()
                time.sleep(.2)
                print("Nao foi possivel manter a conexao com "+conexao.port+"! Verifique a conexao usb.\n")
                if i == len(portlist):
                    return conexao.port, "notconnectado"
                else:
                    i = i+1
    except:
        time.sleep(.2)
        print("Nao foi possivel manter a conexao! Verifique a conexao usb.\n")
        condicaoConeccao = False
        return "0", "notconnectado"

    else:
        if condicaoConeccao == True:
            pass
        else:
            time.sleep(.2)
            print("Nao foi possivel manter a conexao! Verifique a conexao usb.\n")
            condicaoConeccao = False
            return "0", "notconnectado"

#-------------------------------------------------------------------
'''Fim'''
def modeF():
    conexao.write(str(3))  #O valor responsável em parar o ensaio é 3

#-------------------------------------------------------------------
'''Continua'''
def modeC():
    conexao.write(str(1))  #O valor responsável em continuar o ensaio é 1

#-------------------------------------------------------------------
'''Pausa'''
def modeP():
    conexao.write(str(4))  #O valor responsável em pausar o ensaio é 4

#-------------------------------------------------------------------
'''Desconectando'''
def modeD():
    conexao.write(opcaoD)

#-------------------------------------------------------------------
'''Ativando camara'''
def modeE():
    conexao.write(opcaoE)
    while (conexao.inWaiting() == 0):
        pass
    print (conexao.readline())
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())

#-------------------------------------------------------------------
'''Conecxao com a DNIT134'''
def modeI():
    conexao.write(opcaoC)
    conexao.write(opcaoI)
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())

#-------------------------------------------------------------------
'''Aplica os Golpes'''
def modeG(qtd, freq):
    conexao.write(opcaoG)
    while (conexao.inWaiting() == 0):
        pass
    print (conexao.readline())
    conexao.write(str(int(round(qtd,0))))
    while (conexao.inWaiting() == 0):
        pass
    print (conexao.readline())
    time.sleep(1)
    conexao.write(str(int(round(freq,0)))+'\n')
    while (conexao.inWaiting() == 0):
        pass
    print (conexao.readline())

#-------------------------------------------------------------------
'''Camara de ar pressao zero'''
def modeCAMZERO(p1, p1Sen):
    incremental = p1Sen/5
    i = 4
    time.sleep(1)
    while i <= 4 and i >= 0:
        conexao.write(str(int(round((p1 + incremental*i),0))))
        while (conexao.inWaiting() == 0):
            pass
        print (conexao.readline())
        time.sleep(1)
        i = i - 1
        if i == 0:
            conexao.write(str(-1))
            while (conexao.inWaiting() == 0):
                pass
            print (conexao.readline())
            return "p1ok"
            break

#-------------------------------------------------------------------
'''Camara de ar'''
def modeCAM(p1, p1Ant):
    incremental = (p1 - p1Ant)/5
    i = 1
    time.sleep(1)
    while i <= 6:
        conexao.write(str(int(round((p1Ant + incremental*i),0))))
        while (conexao.inWaiting() == 0):
            pass
        print (conexao.readline())
        time.sleep(1)
        i += 1
        if i == 6:
            conexao.write(str(-1))
            return "p1ok"
            break

#-------------------------------------------------------------------
'''Ativando motor'''
def modeM():
    conexao.write(opcaoM)
    while (conexao.inWaiting() == 0):
        pass
    print (conexao.readline())

#-------------------------------------------------------------------
'''Ativando motor'''
def modeBuffer():
    while (conexao.inWaiting() == 0):
        pass
    a = conexao.readline()
    print a
    if a[0] == 'F':
        print "BufferLimpo"
        return True
    else:
        return False

#-------------------------------------------------------------------
'''Ativacao do motor de passos'''
def modeMotor(p2):
    conexao.write(str(int(round(p2,0))))
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())
    contadorOK = 0
    time.sleep(.5)
    while True:
        while (conexao.inWaiting() == 0):
            pass
        a = conexao.readline()
        print a
        try:
            if a[0] == "o":
                contadorOK += 1
                if contadorOK == 25: #contadorOK igual a 25
                    conexao.write(str(1))
                    return "p2ok"
                    break
            '''if a[0] == "n": #if apenas para testes
                conexao.write(str(-1))
                return "p2ok"
                break'''
        except:
            pass

#-------------------------------------------------------------------
'''Limpando Buffer para coleta'''
def Buffer():
    while (conexao.inWaiting() == 0):
        pass
    a = conexao.readline()
    print a
    if a == '\n':
        print "BufferLimpo"
        return True
    if a[0] == 'F':
        print "BufferLimpo"
        return True
    else:
        return False

#-------------------------------------------------------------------
def ColetaI():
    conexao.write(str(0))
    while (conexao.inWaiting() == 0):
        pass
    arduinoString = conexao.readline()
    Array = arduinoString.split(',')
    try:
        y1mm = float(Array[0])*A1+B1
        y2mm = float(Array[1])*A2+B2
        y1v = float(Array[2])
        y2v = float(Array[3])
        sen = float(Array[4])
        cam = float(Array[5])
        glp = float(Array[6])
        sts = float(Array[7])
        defE = float(Array[8])*A1+B1
        defP = float(Array[9])*A1+B1
        defAc = float(Array[10])*A1+B1
        defMax = float(Array[11])*A1+B1
    except:
        y1mm = 0
        y2mm = 0
        y1v = 0
        y2v = 0
        sen = 0
        cam = 0
        glp = 0
        sts = 0
        defE = 0
        defP = 0
        defAc = 0
        defMax = 0


    return y1mm, y2mm, y1v, y2v, sen/10000, cam/10000, glp, sts, defE, defP, defAc, defMax
