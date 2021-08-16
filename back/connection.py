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
conexao.baudrate = 115200

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
    while True:
        while (conexao.inWaiting() == 0):
            pass
        a = conexao.readline()
        if a[0] == 'C':
            print a
            break

#-------------------------------------------------------------------
'''Ativando motor'''
def modeM():
    conexao.write(opcaoM)
    while True:
        while (conexao.inWaiting() == 0):
            pass
        a = conexao.readline()
        if a[0] == 'M':
            print a
            break

#-------------------------------------------------------------------
'''Conecxao com a DNIT134'''
def modeI():
    conexao.write(opcaoC)
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())
    conexao.write(opcaoI)
    while (conexao.inWaiting() == 0):
        pass
    print(conexao.readline())

#-------------------------------------------------------------------
'''Aplica os Golpes'''
def modeG(qtd, freq):
    conexao.write(opcaoG)
    conexao.flushOutput()
    while True:
        while (conexao.inWaiting() == 0):
            pass
        a = conexao.readline()
        print a
        if a[0] == 'G':
            print a
            break

    time.sleep(3)
    conexao.write(str(int(round(qtd,0))))
    while (conexao.inWaiting() == 0):
        pass
    print (conexao.readline())
    time.sleep(1)
    conexao.write(str(int(round(freq,0))))
    while (conexao.inWaiting() == 0):
        pass
    print (conexao.readline())

#-------------------------------------------------------------------
'''Camara de ar pressao zero'''
def modeCAMZERO(p1, p1Sen):
    incremental = p1Sen/5
    i = 4
    time.sleep(1)
    #conexao.flushInput()

    while i <= 4 and i >= 0:
        conexao.write(str(int(round((p1 + incremental*i),0))))
        while (conexao.inWaiting() == 0):
            pass
        print (conexao.readline())
        time.sleep(1)
        i = i - 1
        if i == 0:
            conexao.write(str(-3))
            return "p1ok"
            break

#-------------------------------------------------------------------
'''Camara de ar'''
def modeCAM(p1, p1Ant):
    incremental = (p1 - p1Ant)/5
    i = 1
    time.sleep(1)
    #conexao.flushInput()

    while i <= 6:
        conexao.write(str(int(round((p1Ant + incremental*i),0))))
        while (conexao.inWaiting() == 0):
            pass
        print (conexao.readline())
        time.sleep(1)
        i += 1
        if i == 6:
            conexao.write(str(-3))
            return "p1ok"
            break

#-------------------------------------------------------------------
'''Ativacao do motor de passos'''
def modeMotor(p2):
    conexao.write(str(int(round(p2,0))))
    conexao.flushInput()        #linha que foi adicionada
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
                    conexao.write(str(-3))
                    return "p2ok"
                    break
            '''if a[0] == "n": #if apenas para testes
                conexao.write(str(-3))
                return "p2ok"
                break'''
        except:
            pass

#-------------------------------------------------------------------
def ColetaI(valores):
    while (conexao.inWaiting() == 0):
        pass
    arduinoString = conexao.readline()
    Array = arduinoString.split(',')
    try:
        temp = float(Array[0])
        y1mm = float(Array[1])*A1+B1
        y2mm = float(Array[2])*A2+B2
        y1v = float(Array[3])
        y2v = float(Array[4])
        sen = float(Array[5])
        cam = float(Array[6])
        sts = int(Array[7])
        glp = int(Array[8])

    except:
        temp = valores[0]
        y1mm = valores[1]
        y2mm = valores[2]
        y1v = valores[3]
        y2v = valores[4]
        sen = valores[5]
        cam = valores[6]
        sts = valores[7]
        glp = valores[8]

    return temp, y1mm, y2mm, y1v, y2v, sen/10000, cam/10000, sts, glp
